"""Google OAuth Provider Implementation"""

from datetime import timedelta
from typing import Dict
from urllib.parse import urlencode

import frappe
import requests
from frappe import _
from frappe.utils import get_datetime

from .oauth_base import OAuthProvider

# Google OAuth 2.0 endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

# Required scopes for Google Calendar + Meet
GOOGLE_SCOPES = [
	"https://www.googleapis.com/auth/calendar.events",
	"https://www.googleapis.com/auth/calendar",
	# "https://www.googleapis.com/auth/meetings.space.created",
]


class GoogleOAuthProvider(OAuthProvider):
	"""Google Meet OAuth provider implementation"""

	def get_scopes(self) -> list:
		return GOOGLE_SCOPES

	def get_authorization_url(self, redirect_uri: str) -> str:
		"""
		Generate Google OAuth authorization URL

		Args:
			redirect_uri: OAuth callback URL

		Returns:
			str: Authorization URL to redirect user to
		"""
		if not self.settings.client_id:
			frappe.throw(_("Client ID is not configured in Google Meet settings."))

		# Create state token for security
		state = frappe.generate_hash(length=32)

		# Store state in cache for verification (expires in 10 minutes)
		frappe.cache().set_value(
			f"google_oauth_state:{state}",
			{
				"settings_name": self.settings.name,
				"user": frappe.session.user,
			},
			expires_in_sec=600
		)

		params = {
			"client_id": self.settings.client_id,
			"redirect_uri": redirect_uri,
			"response_type": "code",
			"scope": " ".join(GOOGLE_SCOPES),
			"access_type": "offline",
			"prompt": "consent",
			"state": state,
		}

		return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

	def exchange_code_for_tokens(self, code: str, redirect_uri: str, state: str) -> Dict:
		"""
		Exchange authorization code for access and refresh tokens

		Args:
			code: Authorization code from Google callback
			redirect_uri: Same redirect URI used in authorization request
			state: State token for verification

		Returns:
			dict: Contains success status and message
		"""
		# Verify state token
		cached_state = frappe.cache().get_value(f"google_oauth_state:{state}")

		if not cached_state:
			frappe.throw(_("Invalid or expired state token. Please try authorization again."))

		settings_name = cached_state.get("settings_name")
		expected_user = cached_state.get("user")

		# Clear the state from cache
		frappe.cache().delete_value(f"google_oauth_state:{state}")

		# Verify user matches (security check)
		if frappe.session.user != expected_user:
			frappe.throw(_("User mismatch. Please try authorization again."))

		# Verify settings match
		if settings_name != self.settings.name:
			frappe.throw(_("Settings mismatch. Please try authorization again."))

		client_secret = self.settings.get_password(fieldname="client_secret", raise_exception=False)

		if not client_secret:
			frappe.throw(_("Client Secret is not configured in Google Meet settings."))

		# Exchange code for tokens
		payload = {
			"client_id": self.settings.client_id,
			"client_secret": client_secret,
			"code": code,
			"grant_type": "authorization_code",
			"redirect_uri": redirect_uri,
		}

		response = requests.post(GOOGLE_TOKEN_URL, data=payload)

		if response.status_code != 200:
			error_data = response.json()
			error_msg = error_data.get("error_description", error_data.get("error", "Unknown error"))
			frappe.throw(_("Failed to exchange authorization code: {0}").format(error_msg))

		data = response.json()

		access_token = data.get("access_token")
		refresh_token = data.get("refresh_token")
		expires_in = data.get("expires_in", 3600)

		if not refresh_token:
			frappe.throw(_(
				"No refresh token received. This may happen if the app was previously authorized. "
				"Please revoke access at https://myaccount.google.com/permissions and try again."
			))

		token_expiry = get_datetime() + timedelta(seconds=expires_in)

		# Update settings with tokens
		self.settings.access_token = access_token
		self.settings.token_expiry = token_expiry
		self.settings.refresh_token = refresh_token
		self.settings.save(ignore_permissions=True)
		frappe.db.commit()

		return {
			"success": True,
			"message": _("Google Meet authorization successful! You can now create meetings."),
			"settings_name": settings_name,
		}

	def is_authorized(self) -> bool:
		"""Check if the provider has valid refresh token"""
		refresh_token = self.settings.get_password(fieldname="refresh_token", raise_exception=False)
		return bool(refresh_token)

	def revoke_authorization(self) -> Dict:
		"""Clear stored tokens"""
		self.settings.access_token = None
		self.settings.token_expiry = None
		self.settings.refresh_token = None
		self.settings.save(ignore_permissions=True)
		frappe.db.commit()

		return {
			"success": True,
			"message": _("Google Meet authorization has been revoked."),
		}
