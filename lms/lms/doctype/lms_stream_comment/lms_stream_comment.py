# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LMSStreamComment(Document):
	def before_save(self):
		# Auto-populate user_name from user
		if self.user and not self.user_name:
			self.user_name = frappe.db.get_value("User", self.user, "full_name") or self.user
