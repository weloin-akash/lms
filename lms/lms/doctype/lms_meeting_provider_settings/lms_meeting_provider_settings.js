// Copyright (c) 2025, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("LMS Meeting Provider Settings", {
	refresh(frm) {
		// Show authorization buttons for OAuth providers
		if (!frm.is_new()) {
			if (frm.doc.provider_type === "Google Meet") {
				frm.trigger("setup_oauth_authorization");
			} else if (frm.doc.provider_type === "Microsoft Teams") {
				frm.trigger("setup_oauth_authorization");
			}
		}
	},

	provider_type(frm) {
		// Re-setup buttons when provider type changes
		if (!frm.is_new()) {
			if (frm.doc.provider_type === "Google Meet" || frm.doc.provider_type === "Microsoft Teams") {
				frm.trigger("setup_oauth_authorization");
			} else {
				// Clear dashboard for non-OAuth providers
				frm.dashboard.set_headline("");
				frm.remove_custom_button(__("Authorize"), __("Actions"));
				frm.remove_custom_button(__("Revoke Authorization"), __("Actions"));
				frm.remove_custom_button(__("Check Authorization"), __("Actions"));
			}
		}
	},

	setup_oauth_authorization(frm) {
		const provider_type = frm.doc.provider_type;
		const api_method = provider_type === "Microsoft Teams"
			? "lms.lms.api.microsoft_teams_check_authorization"
			: "lms.lms.api.google_meet_check_authorization";

		// Check authorization status
		frappe.call({
			method: api_method,
			args: {
				settings_name: frm.doc.name,
			},
			callback: function (r) {
				if (r.message) {
					render_authorization_buttons(frm, r.message, provider_type);
				}
			},
		});
	},
});

function render_authorization_buttons(frm, auth_status, provider_type) {
	const provider_name = provider_type === "Microsoft Teams" ? "Microsoft Teams" : "Google Meet";
	const auth_window_name = provider_type === "Microsoft Teams" ? "microsoft_auth" : "google_auth";

	// API methods based on provider
	const api_methods = {
		check: provider_type === "Microsoft Teams"
			? "lms.lms.api.microsoft_teams_check_authorization"
			: "lms.lms.api.google_meet_check_authorization",
		revoke: provider_type === "Microsoft Teams"
			? "lms.lms.api.microsoft_teams_revoke_authorization"
			: "lms.lms.api.google_meet_revoke_authorization",
		get_auth_url: provider_type === "Microsoft Teams"
			? "lms.lms.api.microsoft_teams_get_auth_url"
			: "lms.lms.api.google_meet_get_auth_url",
	};

	// Remove existing buttons first
	frm.remove_custom_button(__("Authorize"), __("Actions"));
	frm.remove_custom_button(__("Revoke Authorization"), __("Actions"));
	frm.remove_custom_button(__("Check Authorization"), __("Actions"));

	if (auth_status.is_authorized) {
		// Show status indicator
		frm.dashboard.set_headline(
			`<span class="indicator green">${__(provider_name + " Authorized")}</span>`
		);

		// Add revoke button
		frm.add_custom_button(
			__("Revoke Authorization"),
			function () {
				frappe.confirm(
					__(
						"Are you sure you want to revoke {0} authorization? You will need to re-authorize to create meetings.",
						[provider_name]
					),
					function () {
						frappe.call({
							method: api_methods.revoke,
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
			`<span class="indicator orange">${__(provider_name + " Not Authorized")}</span>`
		);

		// Add authorize button
		frm.add_custom_button(
			__("Authorize"),
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

				// Check tenant_id for Microsoft Teams
				if (provider_type === "Microsoft Teams" && !frm.doc.tenant_id) {
					frappe.msgprint(
						__(
							"Please enter Tenant ID and save the document before authorizing."
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
					method: api_methods.get_auth_url,
					args: {
						settings_name: frm.doc.name,
					},
					callback: function (r) {
						if (r.message && r.message.authorization_url) {
							// Open authorization URL in new window
							let auth_window = window.open(
								r.message.authorization_url,
								auth_window_name,
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
									"A new window has opened for {0} authorization. Please complete the authorization process and then close that window.",
									[provider_name]
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
				method: api_methods.check,
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
