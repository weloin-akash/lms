"""Microsoft OAuth Provider Implementation"""

from datetime import timedelta
from typing import Dict
from urllib.parse import urlencode

import frappe
import requests
from frappe import _
from frappe.utils import get_datetime

from .oauth_base import OAuthProvider

# Microsoft Azure AD OAuth 2.0 endpoints
# Using 'common' endpoint for multi-tenant support
MICROSOFT_AUTH_URL = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize"
MICROSOFT_TOKEN_URL = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"

# Required scopes for Microsoft Teams meetings
MICROSOFT_SCOPES = [
	"OnlineMeetings.ReadWrite",
	"User.Read",
	"offline_access",
]


class MicrosoftOAuthProvider(OAuthProvider):
	"""Microsoft Teams OAuth provider implementation"""

	def get_scopes(self) -> list:
		return MICROSOFT_SCOPES

	def _get_tenant(self) -> str:
		"""Get tenant ID, defaulting to 'common' for multi-tenant"""
		return self.settings.tenant_id or "common"

	def get_authorization_url(self, redirect_uri: str) -> str:
		"""
		Generate Microsoft OAuth authorization URL

		Args:
			redirect_uri: OAuth callback URL

		Returns:
			str: Authorization URL to redirect user to
		"""
		if not self.settings.client_id:
			frappe.throw(_("Client ID is not configured in Microsoft Teams settings."))

		# Create state token for security
		state = frappe.generate_hash(length=32)

		# Store state in cache for verification (expires in 10 minutes)
		frappe.cache().set_value(
			f"microsoft_oauth_state:{state}",
			{
				"settings_name": self.settings.name,
				"user": frappe.session.user,
			},
			expires_in_sec=600
		)

		tenant = self._get_tenant()
		auth_url = MICROSOFT_AUTH_URL.format(tenant=tenant)

		params = {
			"client_id": self.settings.client_id,
			"redirect_uri": redirect_uri,
			"response_type": "code",
			"scope": " ".join(MICROSOFT_SCOPES),
			"response_mode": "query",
			"state": state,
		}

		return f"{auth_url}?{urlencode(params)}"

	def exchange_code_for_tokens(self, code: str, redirect_uri: str, state: str) -> Dict:
		"""
		Exchange authorization code for access and refresh tokens

		Args:
			code: Authorization code from Microsoft callback
			redirect_uri: Same redirect URI used in authorization request
			state: State token for verification

		Returns:
			dict: Contains success status and message
		"""
		# Verify state token
		cached_state = frappe.cache().get_value(f"microsoft_oauth_state:{state}")

		if not cached_state:
			frappe.throw(_("Invalid or expired state token. Please try authorization again."))

		settings_name = cached_state.get("settings_name")
		expected_user = cached_state.get("user")

		# Clear the state from cache
		frappe.cache().delete_value(f"microsoft_oauth_state:{state}")

		# Verify user matches (security check)
		if frappe.session.user != expected_user:
			frappe.throw(_("User mismatch. Please try authorization again."))

		# Verify settings match
		if settings_name != self.settings.name:
			frappe.throw(_("Settings mismatch. Please try authorization again."))

		client_secret = self.settings.get_password(fieldname="client_secret", raise_exception=False)

		if not client_secret:
			frappe.throw(_("Client Secret is not configured in Microsoft Teams settings."))

		tenant = self._get_tenant()
		token_url = MICROSOFT_TOKEN_URL.format(tenant=tenant)

		# Exchange code for tokens
		payload = {
			"client_id": self.settings.client_id,
			"client_secret": client_secret,
			"code": code,
			"grant_type": "authorization_code",
			"redirect_uri": redirect_uri,
			"scope": " ".join(MICROSOFT_SCOPES),
		}

		response = requests.post(token_url, data=payload)

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
				"No refresh token received. Please ensure 'offline_access' scope is included "
				"and try authorization again."
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
			"message": _("Microsoft Teams authorization successful! You can now create meetings."),
			"settings_name": settings_name,
		}

	def refresh_access_token(self) -> str:
		"""
		Refresh the access token using the refresh token

		Returns:
			str: New access token
		"""
		refresh_token = self.settings.get_password(fieldname="refresh_token", raise_exception=False)

		if not refresh_token:
			frappe.throw(_("No refresh token available. Please authorize Microsoft Teams again."))

		client_secret = self.settings.get_password(fieldname="client_secret", raise_exception=False)

		if not client_secret:
			frappe.throw(_("Client Secret is not configured."))

		tenant = self._get_tenant()
		token_url = MICROSOFT_TOKEN_URL.format(tenant=tenant)

		payload = {
			"client_id": self.settings.client_id,
			"client_secret": client_secret,
			"refresh_token": refresh_token,
			"grant_type": "refresh_token",
			"scope": " ".join(MICROSOFT_SCOPES),
		}

		response = requests.post(token_url, data=payload)

		if response.status_code != 200:
			error_data = response.json()
			error_code = error_data.get("error", "")

			# If refresh token is invalid, clear tokens and require re-authorization
			if error_code in ["invalid_grant", "interaction_required"]:
				self.settings.access_token = None
				self.settings.token_expiry = None
				self.settings.refresh_token = None
				self.settings.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.throw(_(
					"Microsoft Teams authorization has expired. Please authorize again."
				))

			error_msg = error_data.get("error_description", error_code)
			frappe.throw(_("Failed to refresh access token: {0}").format(error_msg))

		data = response.json()

		access_token = data.get("access_token")
		new_refresh_token = data.get("refresh_token", refresh_token)
		expires_in = data.get("expires_in", 3600)

		token_expiry = get_datetime() + timedelta(seconds=expires_in)

		# Update settings with new tokens
		self.settings.access_token = access_token
		self.settings.token_expiry = token_expiry
		self.settings.refresh_token = new_refresh_token
		self.settings.save(ignore_permissions=True)
		frappe.db.commit()

		return access_token

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
			"message": _("Microsoft Teams authorization has been revoked."),
		}
