"""OAuth Provider Factory and Registry"""

import frappe

from .oauth_google import GoogleOAuthProvider
from .oauth_microsoft import MicrosoftOAuthProvider

# Registry of OAuth providers by provider type
OAUTH_PROVIDERS = {
	"Google Meet": GoogleOAuthProvider,
	"Microsoft Teams": MicrosoftOAuthProvider,
}


def get_oauth_provider(settings_name: str):
	"""
	Factory function to get the appropriate OAuth provider instance

	Args:
		settings_name: Name of the LMS Meeting Provider Settings document

	Returns:
		OAuthProvider: Instance of the appropriate OAuth provider class
	"""
	settings = frappe.get_doc("LMS Meeting Provider Settings", settings_name)
	provider_class = OAUTH_PROVIDERS.get(settings.provider_type)

	if not provider_class:
		raise ValueError(f"No OAuth provider available for: {settings.provider_type}")

	return provider_class(settings)


def get_oauth_supported_providers():
	"""Get list of provider types that support OAuth"""
	return list(OAUTH_PROVIDERS.keys())


def provider_requires_oauth(provider_type: str) -> bool:
	"""Check if a provider type requires OAuth authorization"""
	return provider_type in OAUTH_PROVIDERS
