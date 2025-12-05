import frappe
import base64
import json
import requests
from frappe.model.document import Document
from datetime import timedelta
from frappe.utils import format_datetime , get_time, cint
                    
#Zoom Live Class Create
@frappe.whitelist()
def create_live_class(batch_name,zoom_account,title,duration,date,time,timezone,auto_recording,description = None):
        payload = {
                "topic": title,
                "start_time": format_datetime(f"{date} {time}", "yyyy-MM-ddTHH:mm:ssZ"),
                "duration": duration,
                "agenda": description,
                "private_meeting": True,
                "auto_recording": "none" if auto_recording == "No Recording" else auto_recording.lower(),
                "timezone": timezone,
            }
        headers = {
                "Authorization": "Bearer " + 
                (zoom_account),
                "content-type": "application/json",
            }
        response = requests.post(
                "https://api.zoom.us/v2/users/me/meetings", headers=headers, data=json.dumps(payload)
            )
        if response.status_code == 201:
                data = json.loads(response.text)
                payload.update(
                    {
                        "doctype": "LMS Live Class",
                        "start_url": data.get("start_url"),
                        "join_url": data.get("join_url"),
                        "meeting_id": data.get("id"),
                        "uuid": data.get("uuid"),
                        "title": title,
                        "host": frappe.session.user,
                        "date": date,
                        "time": time,
                        "batch_name": batch_name,
                        "password": data.get("password"),
                        "description": description,
                        "auto_recording": auto_recording,
                        "zoom_account": zoom_account,
                    }
                )
                class_details = frappe.get_doc(payload)
                class_details.save()
                return class_details
        else:
            frappe.throw(_("Error creating live class. Please try again. {0}").format(response.text))

#Zoom Account Enable Authenticate 
def authenticate(zoom_account):
    zoom = frappe.get_doc(zoom_account)
    if not zoom.enabled:
        frappe.throw(_("Please Activate Your Zoom Account"))
    authenticate_url = (
		f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={zoom.account_id}"
	)   

    headers = {
		"Authorization": "Basic "
		+ base64.b64encode(
			bytes(
				zoom.client_id + ":" + zoom.get_password(fieldname="client_secret", raise_exception=False),
				encoding="utf8",
			).decode()
        )
    }
    response = requests.post(authenticate_url ,  headers = headers)
    return response
    