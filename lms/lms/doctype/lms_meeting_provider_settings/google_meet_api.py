"""Google Meet API for creating and managing meetings"""

from datetime import timedelta
from typing import Dict, Optional

import frappe
import requests
from frappe import _
from frappe.utils import get_datetime

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_MEET_API_URL = "https://meet.googleapis.com/v2"


def get_valid_access_token(settings_name: str) -> str:
	"""
	Get a valid access token, refreshing if necessary.

	Args:
		settings_name: Name of the LMS Meeting Provider Settings document

	Returns:
		str: Valid access token

	Raises:
		frappe.ValidationError: If unable to get valid token
	"""
	settings = frappe.get_doc("LMS Meeting Provider Settings", settings_name)

	if settings.provider_type != "Google Meet":
		frappe.throw(_("This settings document is not configured for Google Meet"))

	refresh_token = settings.get_password(fieldname="refresh_token", raise_exception=False)
	if not refresh_token:
		frappe.throw(_(
			"Google Meet is not authorized. Please complete OAuth authorization first."
		))

	access_token = settings.get_password(fieldname="access_token", raise_exception=False)
	token_expiry = settings.token_expiry

	if access_token and token_expiry:
		if get_datetime(token_expiry) > get_datetime() + timedelta(minutes=5):
			return access_token

	return _refresh_access_token(settings, refresh_token)


def _refresh_access_token(settings, refresh_token: str) -> str:
	"""
	Refresh the access token using the refresh token.

	Args:
		settings: LMS Meeting Provider Settings document
		refresh_token: The refresh token

	Returns:
		str: New access token
	"""
	client_secret = settings.get_password(fieldname="client_secret", raise_exception=False)

	if not client_secret:
		frappe.throw(_("Client Secret is not configured"))

	payload = {
		"client_id": settings.client_id,
		"client_secret": client_secret,
		"refresh_token": refresh_token,
		"grant_type": "refresh_token",
	}

	response = requests.post(GOOGLE_TOKEN_URL, data=payload)

	if response.status_code != 200:
		error_data = response.json()
		error_msg = error_data.get("error_description", error_data.get("error", "Unknown error"))

		if "invalid_grant" in str(error_data.get("error", "")):
			settings.access_token = None
			settings.token_expiry = None
			settings.refresh_token = None
			settings.save(ignore_permissions=True)
			frappe.db.commit()
			frappe.throw(_(
				"Google authorization has expired. Please re-authorize Google Meet."
			))

		frappe.throw(_("Failed to refresh access token: {0}").format(error_msg))

	data = response.json()
	access_token = data.get("access_token")
	expires_in = data.get("expires_in", 3600)
	token_expiry = get_datetime() + timedelta(seconds=expires_in)

	settings.access_token = access_token
	settings.token_expiry = token_expiry
	settings.save(ignore_permissions=True)
	frappe.db.commit()

	return access_token


@frappe.whitelist(allow_guest=True)
def create_meeting_space(
	settings_name: str,
	display_name: Optional[str] = None,
	start_time: Optional[str] = None,
	end_time: Optional[str] = None,
) -> Dict:
	"""
	Create a new Google Meet meeting space using Google Calendar API.

	Args:
		settings_name: Name of the LMS Meeting Provider Settings document
		display_name: Optional display name for the meeting
		start_time: Optional start time in ISO format (defaults to now)
		end_time: Optional end time in ISO format (defaults to start_time + 1 hour)

	Returns:
		dict: Meeting space details including:
			- event_id: Calendar event ID
			- meeting_uri: URL to join the meeting
			- meeting_code: Meeting code for joining
			- html_link: Link to the calendar event
	"""
	access_token = get_valid_access_token(settings_name)

	headers = {
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json",
	}

	if not start_time:
		start_time = get_datetime().isoformat()
	if not end_time:
		end_time = (get_datetime() + timedelta(hours=1)).isoformat()

	event = {
		"summary": display_name or "Google Meet",
		"start": {
			"dateTime": start_time,
			"timeZone": frappe.db.get_single_value("System Settings", "time_zone") or "UTC",
		},
		"end": {
			"dateTime": end_time,
			"timeZone": frappe.db.get_single_value("System Settings", "time_zone") or "UTC",
		},
		"conferenceData": {
			"createRequest": {
				"requestId": frappe.generate_hash(length=16),
				"conferenceSolutionKey": {
					"type": "hangoutsMeet"
				}
			}
		},
	}

	params = {
		"conferenceDataVersion": 1,
		"sendUpdates": "none",
	}

	response = requests.post(
		"https://www.googleapis.com/calendar/v3/calendars/primary/events",
		headers=headers,
		params=params,
		json=event,
	)

	if response.status_code not in [200, 201]:
		error_data = response.json() if response.content else {}
		error_msg = error_data.get("error", {}).get("message", "Unknown error")
		frappe.throw(_("Failed to create meeting space: {0}").format(error_msg))

	data = response.json()

	conference_data = data.get("conferenceData", {})
	entry_points = conference_data.get("entryPoints", [])
	meet_uri = None
	meeting_code = None

	for entry in entry_points:
		if entry.get("entryPointType") == "video":
			meet_uri = entry.get("uri")
			if meet_uri and "/" in meet_uri:
				meeting_code = meet_uri.split("/")[-1]
			break

	return {
		"success": True,
		"event_id": data.get("id"),
		"meeting_uri": meet_uri,
		"meeting_code": meeting_code or conference_data.get("conferenceId"),
		"html_link": data.get("htmlLink"),
	}


@frappe.whitelist()
def schedule_meeting(
	settings_name: str,
	title: str,
	start_time: str,
	end_time: str,
	description: Optional[str] = None,
	attendees: Optional[list] = None,
	send_notifications: bool = True,
) -> Dict:
	"""
	Schedule a meeting with Google Meet link using Google Calendar API.

	This creates a calendar event with an automatically generated Google Meet link.

	Args:
		settings_name: Name of the LMS Meeting Provider Settings document
		title: Meeting title
		start_time: Start time in ISO format (e.g., "2025-01-15T10:00:00")
		end_time: End time in ISO format (e.g., "2025-01-15T11:00:00")
		description: Optional meeting description
		attendees: Optional list of attendee email addresses
		send_notifications: Whether to send email notifications to attendees

	Returns:
		dict: Meeting details including:
			- event_id: Calendar event ID
			- meeting_uri: URL to join the Google Meet
			- html_link: Link to the calendar event
	"""
	access_token = get_valid_access_token(settings_name)

	headers = {
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json",
	}

	if isinstance(attendees, str):
		import json
		try:
			attendees = json.loads(attendees)
		except (json.JSONDecodeError, TypeError):
			attendees = []

	event = {
		"summary": title,
		"start": {
			"dateTime": start_time,
			"timeZone": frappe.db.get_single_value("System Settings", "time_zone") or "UTC",
		},
		"end": {
			"dateTime": end_time,
			"timeZone": frappe.db.get_single_value("System Settings", "time_zone") or "UTC",
		},
		"conferenceData": {
			"createRequest": {
				"requestId": frappe.generate_hash(length=16),
				"conferenceSolutionKey": {
					"type": "hangoutsMeet"
				}
			}
		},
	}

	if description:
		event["description"] = description

	if attendees:
		event["attendees"] = [{"email": email} for email in attendees]

	params = {
		"conferenceDataVersion": 1,
		"sendUpdates": "all" if send_notifications else "none",
	}

	response = requests.post(
		"https://www.googleapis.com/calendar/v3/calendars/primary/events",
		headers=headers,
		params=params,
		json=event,
	)

	if response.status_code not in [200, 201]:
		error_data = response.json() if response.content else {}
		error_msg = error_data.get("error", {}).get("message", "Unknown error")
		frappe.throw(_("Failed to schedule meeting: {0}").format(error_msg))

	data = response.json()


	conference_data = data.get("conferenceData", {})
	entry_points = conference_data.get("entryPoints", [])
	meet_uri = None

	for entry in entry_points:
		if entry.get("entryPointType") == "video":
			meet_uri = entry.get("uri")
			break

	return {
		"success": True,
		"event_id": data.get("id"),
		"meeting_uri": meet_uri,
		"html_link": data.get("htmlLink"),
		"conference_id": conference_data.get("conferenceId"),
	}


# @frappe.whitelist()
# def get_meeting_space(settings_name: str, space_name: str) -> Dict:
# 	"""
# 	Get details of an existing meeting space.

# 	Args:
# 		settings_name: Name of the LMS Meeting Provider Settings document
# 		space_name: The space resource name (e.g., "spaces/abc123")

# 	Returns:
# 		dict: Meeting space details
# 	"""
# 	access_token = get_valid_access_token(settings_name)

# 	headers = {
# 		"Authorization": f"Bearer {access_token}",
# 	}

# 	response = requests.get(
# 		f"{GOOGLE_MEET_API_URL}/{space_name}",
# 		headers=headers,
# 	)

# 	if response.status_code != 200:
# 		error_data = response.json() if response.content else {}
# 		error_msg = error_data.get("error", {}).get("message", "Unknown error")
# 		frappe.throw(_("Failed to get meeting space: {0}").format(error_msg))

# 	data = response.json()

# 	return {
# 		"success": True,
# 		"name": data.get("name"),
# 		"meeting_uri": data.get("meetingUri"),
# 		"meeting_code": data.get("meetingCode"),
# 		"config": data.get("config", {}),
# 	}


# @frappe.whitelist()
# def end_active_conference(settings_name: str, space_name: str) -> Dict:
# 	"""
# 	End an active conference in a meeting space.

# 	Args:
# 		settings_name: Name of the LMS Meeting Provider Settings document
# 		space_name: The space resource name (e.g., "spaces/abc123")

# 	Returns:
# 		dict: Success status
# 	"""
# 	access_token = get_valid_access_token(settings_name)

# 	headers = {
# 		"Authorization": f"Bearer {access_token}",
# 		"Content-Type": "application/json",
# 	}

# 	response = requests.post(
# 		f"{GOOGLE_MEET_API_URL}/{space_name}:endActiveConference",
# 		headers=headers,
# 		json={},
# 	)

# 	if response.status_code not in [200, 204]:
# 		error_data = response.json() if response.content else {}
# 		error_msg = error_data.get("error", {}).get("message", "Unknown error")
# 		frappe.throw(_("Failed to end conference: {0}").format(error_msg))

# 	return {
# 		"success": True,
# 		"message": _("Conference ended successfully"),
# 	}
