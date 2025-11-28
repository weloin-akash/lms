// Copyright (c) 2025, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("LMS Meeting Provider Settings", {
	refresh(frm) {
		// Only show authorization buttons for Google Meet
		if (frm.doc.provider_type === "Google Meet" && !frm.is_new()) {
			frm.trigger("setup_google_meet_authorization");
		}
	},

	provider_type(frm) {
		// Re-setup buttons when provider type changes
		if (frm.doc.provider_type === "Google Meet" && !frm.is_new()) {
			frm.trigger("setup_google_meet_authorization");
		}
	},

	setup_google_meet_authorization(frm) {
		// Check authorization status
		frappe.call({
			method: "lms.lms.api.google_meet_check_authorization",
			args: {
				settings_name: frm.doc.name,
			},
			callback: function (r) {
				if (r.message) {
					render_authorization_buttons(frm, r.message);
				}
			},
		});
	},
});

function render_authorization_buttons(frm, auth_status) {
	// Remove existing buttons first
	frm.remove_custom_button(__("Authorize Google Meet"), __("Actions"));
	frm.remove_custom_button(__("Revoke Authorization"), __("Actions"));
	frm.remove_custom_button(__("Check Authorization"), __("Actions"));

	if (auth_status.is_authorized) {
		// Show status indicator
		frm.dashboard.set_headline(
			`<span class="indicator green">${__("Google Meet Authorized")}</span>`
		);

		// Add revoke button
		frm.add_custom_button(
			__("Revoke Authorization"),
			function () {
				frappe.confirm(
					__(
						"Are you sure you want to revoke Google Meet authorization? You will need to re-authorize to create meetings."
					),
					function () {
						frappe.call({
							method: "lms.lms.api.google_meet_revoke_authorization",
							args: {
								settings_name: frm.doc.name,
							},
							callback: function (r) {
								if (r.message && r.message.success) {
									frappe.msgprint(r.message.message);
									frm.reload_doc();
								}
							},
						});
					}
				);
			},
			__("Actions")
		);
	} else {
		// Show status indicator
		frm.dashboard.set_headline(
			`<span class="indicator orange">${__("Google Meet Not Authorized")}</span>`
		);

		// Add authorize button
		frm.add_custom_button(
			__("Authorize Google Meet"),
			function () {
				// Check if document is saved with client_id and client_secret
				if (!frm.doc.client_id || !frm.doc.client_secret) {
					frappe.msgprint(
						__(
							"Please enter Client ID and Client Secret and save the document before authorizing."
						)
					);
					return;
				}

				if (frm.is_dirty()) {
					frappe.msgprint(
						__("Please save the document before authorizing.")
					);
					return;
				}

				frappe.call({
					method: "lms.lms.api.google_meet_get_auth_url",
					args: {
						settings_name: frm.doc.name,
					},
					callback: function (r) {
						if (r.message && r.message.authorization_url) {
							// Open authorization URL in new window
							let auth_window = window.open(
								r.message.authorization_url,
								"google_auth",
								"width=600,height=700"
							);

							// Poll to check if authorization completed
							let poll_interval = setInterval(function () {
								if (auth_window.closed) {
									clearInterval(poll_interval);
									// Reload form to check new authorization status
									frm.reload_doc();
								}
							}, 1000);

							frappe.msgprint({
								title: __("Authorization"),
								message: __(
									"A new window has opened for Google authorization. Please complete the authorization process and then close that window."
								),
								indicator: "blue",
							});
						}
					},
				});
			},
			__("Actions")
		);
	}

	// Add check authorization button (useful for debugging)
	frm.add_custom_button(
		__("Check Authorization"),
		function () {
			frappe.call({
				method: "lms.lms.api.google_meet_check_authorization",
				args: {
					settings_name: frm.doc.name,
				},
				callback: function (r) {
					if (r.message) {
						frappe.msgprint({
							title: __("Authorization Status"),
							message: r.message.message,
							indicator: r.message.is_authorized ? "green" : "orange",
						});
						frm.reload_doc();
					}
				},
			});
		},
		__("Actions")
	);
}
