# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe
import secrets
from frappe import _
from frappe.model.document import Document


class LMSBroadcastStream(Document):
    def before_insert(self):
        """Generate stream key and URLs before creating document."""
        self.generate_stream_config()

    def generate_stream_config(self):
        """Generate unique stream key and set URLs for both OBS and browser streaming."""
        # Get server config from LMS Settings
        media_server = frappe.db.get_single_value("LMS Settings", "media_server_host") or "localhost"

        # Generate unique stream key
        self.stream_key = secrets.token_urlsafe(16)

        # OBS streaming (RTMP) - same format for SRS
        rtmp_port = frappe.db.get_single_value("LMS Settings", "rtmp_port") or "1935"
        self.rtmp_url = f"rtmp://{media_server}:{rtmp_port}/live"

        # Browser streaming (WebRTC) - SRS format
        webrtc_port = frappe.db.get_single_value("LMS Settings", "webrtc_port") or "1985"
        webrtc_protocol = "https" if frappe.db.get_single_value("LMS Settings", "use_ssl") else "http"
        # SRS WebRTC publish URL format
        self.webrtc_url = f"{webrtc_protocol}://{media_server}:{webrtc_port}/rtc/v1/whip/?app=live&stream={self.stream_key}"

        # Playback URLs - SRS format
        http_port = frappe.db.get_single_value("LMS Settings", "hls_port") or "8080"
        http_protocol = "https" if frappe.db.get_single_value("LMS Settings", "use_ssl") else "http"
        # HTTP-FLV for low latency (~2-5s)
        self.playback_url = f"{http_protocol}://{media_server}:{http_port}/live/{self.stream_key}.flv"
        # HLS as fallback (higher latency ~10-20s)
        self.hls_url = f"{http_protocol}://{media_server}:{http_port}/live/{self.stream_key}.m3u8"

    def on_update(self):
        """Notify viewers when stream status changes."""
        if self.has_value_changed("status"):
            self.broadcast_status_change()

    def broadcast_status_change(self):
        """Send real-time update to all viewers."""
        frappe.publish_realtime(
            event="stream_status_changed",
            message={
                "stream": self.name,
                "status": self.status,
                "playback_url": self.playback_url
            },
            doctype=self.doctype,
            docname=self.name
        )
