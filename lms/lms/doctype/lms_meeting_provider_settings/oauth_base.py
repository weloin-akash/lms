"""Base OAuth Provider Interface"""

from abc import ABC, abstractmethod
from typing import Dict


class OAuthProvider(ABC):
	"""Abstract base class for OAuth providers"""

	def __init__(self, settings_doc):
		"""
		Initialize the OAuth provider with settings document

		Args:
			settings_doc: LMS Meeting Provider Settings document
		"""
		self.settings = settings_doc

	@abstractmethod
	def get_authorization_url(self, redirect_uri: str) -> str:
		"""
		Generate OAuth authorization URL

		Args:
			redirect_uri: Callback URL after authorization

		Returns:
			str: Authorization URL to redirect user to
		"""
		pass

	@abstractmethod
	def exchange_code_for_tokens(self, code: str, redirect_uri: str, state: str) -> Dict:
		"""
		Exchange authorization code for access and refresh tokens

		Args:
			code: Authorization code from provider callback
			redirect_uri: Same redirect URI used in authorization request
			state: State token for verification

		Returns:
			dict: Contains success status, message, and tokens
		"""
		pass

	@abstractmethod
	def is_authorized(self) -> bool:
		"""
		Check if the provider has valid authorization

		Returns:
			bool: True if authorized
		"""
		pass

	@abstractmethod
	def revoke_authorization(self) -> Dict:
		"""
		Revoke/clear stored authorization tokens

		Returns:
			dict: Success status and message
		"""
		pass

	@abstractmethod
	def get_scopes(self) -> list:
		"""
		Get required OAuth scopes for this provider

		Returns:
			list: List of scope strings
		"""
		pass
