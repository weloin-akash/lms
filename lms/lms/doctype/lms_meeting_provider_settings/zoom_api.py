"""Zoom API for creating and managing meetings"""

import base64
import json
from typing import Dict, Optional

import frappe
import requests
from frappe import _
from frappe.utils import format_datetime

ZOOM_TOKEN_URL = "https://zoom.us/oauth/token"
ZOOM_API_URL = "https://api.zoom.us/v2"


def get_valid_access_token(settings_name: str) -> str:
	"""
	Get a valid access token using Zoom Server-to-Server OAuth.

	Args:
		settings_name: Name of the LMS Meeting Provider Settings document

	Returns:
		str: Valid access token

	Raises:
		frappe.ValidationError: If unable to get valid token
	"""
	settings = frappe.get_doc("LMS Meeting Provider Settings", settings_name)

	if settings.provider_type != "Zoom":
		frappe.throw(_("This settings document is not configured for Zoom"))

	if not settings.enabled:
		frappe.throw(_("Please enable the Zoom account to use this feature."))

	if not settings.account_id:
		frappe.throw(_("Account ID is required for Zoom Server-to-Server OAuth"))

	client_secret = settings.get_password(fieldname="client_secret", raise_exception=False)
	if not client_secret:
		frappe.throw(_("Client Secret is not configured"))

	# Zoom Server-to-Server OAuth - get new token each time (or implement caching)
	authenticate_url = f"{ZOOM_TOKEN_URL}?grant_type=account_credentials&account_id={settings.account_id}"

	credentials = f"{settings.client_id}:{client_secret}"
	encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode()

	headers = {
		"Authorization": f"Basic {encoded_credentials}",
		"Content-Type": "application/x-www-form-urlencoded",
	}

	response = requests.post(authenticate_url, headers=headers)

	if response.status_code != 200:
		error_data = response.json() if response.content else {}
		error_msg = error_data.get("reason", error_data.get("error", "Unknown error"))
		frappe.throw(_("Failed to authenticate with Zoom: {0}").format(error_msg))

	data = response.json()
	return data.get("access_token")


@frappe.whitelist()
def create_meeting(
	settings_name: str,
	title: str,
	start_time: str,
	duration: int,
	timezone: str,
	description: Optional[str] = None,
	auto_recording: str = "none",
) -> Dict:
	"""
	Create a new Zoom meeting.

	Args:
		settings_name: Name of the LMS Meeting Provider Settings document
		title: Meeting title/topic
		start_time: Start time in ISO format (e.g., "2025-01-15T10:00:00")
		duration: Duration in minutes
		timezone: Timezone for the meeting
		description: Optional meeting description/agenda
		auto_recording: Recording option - "none", "local", or "cloud"

	Returns:
		dict: Meeting details including:
			- meeting_id: Zoom meeting ID
			- start_url: URL for host to start the meeting
			- join_url: URL for participants to join
			- password: Meeting password
	"""
	access_token = get_valid_access_token(settings_name)

	headers = {
		"Authorization": f"Bearer {access_token}",
		"Content-Type": "application/json",
	}

	# Format auto_recording
	if auto_recording == "No Recording":
		auto_recording = "none"
	elif auto_recording in ["Local", "Cloud"]:
		auto_recording = auto_recording.lower()

	payload = {
		"topic": title,
		"type": 2,  # Scheduled meeting
		"start_time": start_time,
		"duration": int(duration),
		"timezone": timezone,
		"agenda": description or "",
		"settings": {
			"host_video": True,
			"participant_video": True,
			"join_before_host": False,
			"mute_upon_entry": True,
			"auto_recording": auto_recording,
			"waiting_room": True,
		},
	}

	response = requests.post(
		f"{ZOOM_API_URL}/users/me/meetings",
		headers=headers,
		data=json.dumps(payload),
	)

	if response.status_code not in [200, 201]:
		error_data = response.json() if response.content else {}
		error_msg = error_data.get("message", error_data.get("error", "Unknown error"))
		frappe.throw(_("Failed to create Zoom meeting: {0}").format(error_msg))

	data = response.json()

	return {
		"success": True,
		"meeting_id": str(data.get("id")),
		"uuid": data.get("uuid"),
		"start_url": data.get("start_url"),
		"join_url": data.get("join_url"),
		"password": data.get("password"),
		"host_email": data.get("host_email"),
	}


@frappe.whitelist()
def schedule_meeting(
	settings_name: str,
	title: str,
	start_time: str,
	end_time: str,
	description: Optional[str] = None,
	timezone: Optional[str] = None,
	auto_recording: str = "none",
) -> Dict:
	"""
	Schedule a Zoom meeting (wrapper for create_meeting with end_time calculation).

	This is the main function called by create_meeting_provider_class for consistency
	with Google Meet API.

	Args:
		settings_name: Name of the LMS Meeting Provider Settings document
		title: Meeting title
		start_time: Start time in ISO format
		end_time: End time in ISO format (used to calculate duration)
		description: Optional meeting description
		timezone: Optional timezone (extracted from start_time if not provided)
		auto_recording: Recording option

	Returns:
		dict: Meeting details
	"""
	from datetime import datetime

	# Parse times to calculate duration
	# Handle ISO format with timezone
	start_dt_str = start_time.replace("Z", "+00:00")
	end_dt_str = end_time.replace("Z", "+00:00")

	# Try parsing with timezone info
	try:
		if "+" in start_dt_str or "-" in start_dt_str[10:]:
			start_dt = datetime.fromisoformat(start_dt_str)
			end_dt = datetime.fromisoformat(end_dt_str)
		else:
			start_dt = datetime.fromisoformat(start_dt_str)
			end_dt = datetime.fromisoformat(end_dt_str)
	except ValueError:
		# Fallback for simpler format
		start_dt = datetime.strptime(start_time[:19], "%Y-%m-%dT%H:%M:%S")
		end_dt = datetime.strptime(end_time[:19], "%Y-%m-%dT%H:%M:%S")

	duration = int((end_dt - start_dt).total_seconds() / 60)

	# Get timezone from settings if not provided
	if not timezone:
		timezone = frappe.db.get_single_value("System Settings", "time_zone") or "UTC"

	# Format start_time for Zoom API (needs specific format)
	zoom_start_time = start_time

	result = create_meeting(
		settings_name=settings_name,
		title=title,
		start_time=zoom_start_time,
		duration=duration,
		timezone=timezone,
		description=description,
		auto_recording=auto_recording,
	)

	# Map to consistent response format with Google Meet
	return {
		"success": result.get("success"),
		"event_id": result.get("meeting_id"),
		"meeting_uri": result.get("join_url"),
		"html_link": result.get("start_url"),
		"meeting_id": result.get("meeting_id"),
		"uuid": result.get("uuid"),
		"start_url": result.get("start_url"),
		"join_url": result.get("join_url"),
		"password": result.get("password"),
	}


@frappe.whitelist()
def get_meeting(settings_name: str, meeting_id: str) -> Dict:
	"""
	Get details of an existing Zoom meeting.

	Args:
		settings_name: Name of the LMS Meeting Provider Settings document
		meeting_id: The Zoom meeting ID

	Returns:
		dict: Meeting details
	"""
	access_token = get_valid_access_token(settings_name)

	headers = {
		"Authorization": f"Bearer {access_token}",
	}

	response = requests.get(
		f"{ZOOM_API_URL}/meetings/{meeting_id}",
		headers=headers,
	)

	if response.status_code != 200:
		error_data = response.json() if response.content else {}
		error_msg = error_data.get("message", error_data.get("error", "Unknown error"))
		frappe.throw(_("Failed to get Zoom meeting: {0}").format(error_msg))

	data = response.json()

	return {
		"success": True,
		"meeting_id": str(data.get("id")),
		"topic": data.get("topic"),
		"start_url": data.get("start_url"),
		"join_url": data.get("join_url"),
		"status": data.get("status"),
		"start_time": data.get("start_time"),
		"duration": data.get("duration"),
	}


@frappe.whitelist()
def delete_meeting(settings_name: str, meeting_id: str) -> Dict:
	"""
	Delete a Zoom meeting.

	Args:
		settings_name: Name of the LMS Meeting Provider Settings document
		meeting_id: The Zoom meeting ID

	Returns:
		dict: Success status
	"""
	access_token = get_valid_access_token(settings_name)

	headers = {
		"Authorization": f"Bearer {access_token}",
	}

	response = requests.delete(
		f"{ZOOM_API_URL}/meetings/{meeting_id}",
		headers=headers,
	)

	if response.status_code not in [200, 204]:
		error_data = response.json() if response.content else {}
		error_msg = error_data.get("message", error_data.get("error", "Unknown error"))
		frappe.throw(_("Failed to delete Zoom meeting: {0}").format(error_msg))

	return {
		"success": True,
		"message": _("Meeting deleted successfully"),
	}
