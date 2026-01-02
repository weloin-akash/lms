"""Microsoft Teams API for creating and managing online meetings"""

from datetime import timedelta
from typing import Dict, Optional

import frappe
import requests
from frappe import _
from frappe.utils import get_datetime

# Microsoft Graph API endpoint
GRAPH_API_URL = "https://graph.microsoft.com/v1.0"


def get_valid_access_token(settings_name: str) -> str:
	"""
	Get a valid access token, refreshing if needed.

	Args:
		settings_name: Name of the LMS Meeting Provider Settings document

	Returns:
		str: Valid access token

	Raises:
		frappe.ValidationError: If unable to get valid token
	"""
	settings = frappe.get_doc("LMS Meeting Provider Settings", settings_name)

	if settings.provider_type != "Microsoft Teams":
		frappe.throw(_("This settings document is not configured for Microsoft Teams"))

	if not settings.enabled:
		frappe.throw(_("Please enable the Microsoft Teams account to use this feature."))

	# Check if we have a valid access token
	access_token = settings.get_password(fieldname="access_token", raise_exception=False)
	token_expiry = settings.token_expiry

	# If token exists and not expiring within 5 minutes, use it
	if access_token and token_expiry:
		if get_datetime(token_expiry) > get_datetime() + timedelta(minutes=5):
			return access_token

	# Need to refresh token
	from .oauth_microsoft import MicrosoftOAuthProvider

	provider = MicrosoftOAuthProvider(settings)
	return provider.refresh_access_token()


@frappe.whitelist()
def create_meeting(
	settings_name: str,
	title: str,
	start_time: str,
	end_time: str,
	description: Optional[str] = None,
) -> Dict:
	"""
	Create a new Microsoft Teams online meeting.

	Args:
		settings_name: Name of the LMS Meeting Provider Settings document
		title: Meeting subject/title
		start_time: Start time in ISO format (e.g., "2025-01-15T10:00:00")
		end_time: End time in ISO format
		description: Optional meeting description

	Returns:
		dict: Meeting details including:
			- meeting_id: Teams meeting ID
			- join_url: URL for participants to join
			- subject: Meeting subject
	"""
	access_token = get_valid_access_token(settings_name)

	headers = {
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json",
	}

	payload = {
		"subject": title,
		"startDateTime": start_time,
		"endDateTime": end_time,
	}

	# Add lobby bypass settings for easier access
	payload["lobbyBypassSettings"] = {
		"scope": "organization",
		"isDialInBypassEnabled": True,
	}

	# Add auto-admit settings
	payload["autoAdmittedUsers"] = "everyone"

	response = requests.post(
		f"{GRAPH_API_URL}/me/onlineMeetings",
		headers=headers,
		json=payload,
	)

	if response.status_code not in [200, 201]:
		error_data = response.json() if response.content else {}
		error_msg = error_data.get("error", {}).get("message", "Unknown error")
		frappe.throw(_("Failed to create Microsoft Teams meeting: {0}").format(error_msg))

	data = response.json()

	return {
		"success": True,
		"meeting_id": data.get("id"),
		"join_url": data.get("joinWebUrl"),
		"subject": data.get("subject"),
		"start_time": data.get("startDateTime"),
		"end_time": data.get("endDateTime"),
		"video_teleconference_id": data.get("videoTeleconferenceId"),
	}


@frappe.whitelist()
def schedule_meeting(
	settings_name: str,
	title: str,
	start_time: str,
	end_time: str,
	description: Optional[str] = None,
) -> Dict:
	"""
	Schedule a Microsoft Teams meeting.

	This is the main function called by create_meeting_provider_class for consistency
	with Google Meet and Zoom APIs.

	Args:
		settings_name: Name of the LMS Meeting Provider Settings document
		title: Meeting title
		start_time: Start time in ISO format
		end_time: End time in ISO format
		description: Optional meeting description

	Returns:
		dict: Meeting details in standardized format
	"""
	result = create_meeting(
		settings_name=settings_name,
		title=title,
		start_time=start_time,
		end_time=end_time,
		description=description,
	)

	# Map to consistent response format with Google Meet and Zoom
	return {
		"success": result.get("success"),
		"event_id": result.get("meeting_id"),
		"meeting_uri": result.get("join_url"),
		"html_link": result.get("join_url"),
		"meeting_id": result.get("meeting_id"),
		"join_url": result.get("join_url"),
		"start_url": result.get("join_url"),  # Teams uses same URL for host
	}


@frappe.whitelist()
def get_meeting(settings_name: str, meeting_id: str) -> Dict:
	"""
	Get details of an existing Microsoft Teams meeting.

	Args:
		settings_name: Name of the LMS Meeting Provider Settings document
		meeting_id: The Teams meeting ID

	Returns:
		dict: Meeting details
	"""
	access_token = get_valid_access_token(settings_name)

	headers = {
		"Authorization": f"Bearer {access_token}",
	}

	response = requests.get(
		f"{GRAPH_API_URL}/me/onlineMeetings/{meeting_id}",
		headers=headers,
	)

	if response.status_code != 200:
		error_data = response.json() if response.content else {}
		error_msg = error_data.get("error", {}).get("message", "Unknown error")
		frappe.throw(_("Failed to get Microsoft Teams meeting: {0}").format(error_msg))

	data = response.json()

	return {
		"success": True,
		"meeting_id": data.get("id"),
		"subject": data.get("subject"),
		"join_url": data.get("joinWebUrl"),
		"start_time": data.get("startDateTime"),
		"end_time": data.get("endDateTime"),
	}


@frappe.whitelist()
def delete_meeting(settings_name: str, meeting_id: str) -> Dict:
	"""
	Delete a Microsoft Teams meeting.

	Args:
		settings_name: Name of the LMS Meeting Provider Settings document
		meeting_id: The Teams meeting ID

	Returns:
		dict: Success status
	"""
	access_token = get_valid_access_token(settings_name)

	headers = {
		"Authorization": f"Bearer {access_token}",
	}

	response = requests.delete(
		f"{GRAPH_API_URL}/me/onlineMeetings/{meeting_id}",
		headers=headers,
	)

	if response.status_code not in [200, 204]:
		error_data = response.json() if response.content else {}
		error_msg = error_data.get("error", {}).get("message", "Unknown error")
		frappe.throw(_("Failed to delete Microsoft Teams meeting: {0}").format(error_msg))

	return {
		"success": True,
		"message": _("Meeting deleted successfully"),
	}
