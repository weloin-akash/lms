import requests
import json

CLIENT_ID = "<YOUR_CLIENT_ID>"
CLIENT_SECRET = "<YOUR_CLIENT_SECRET>"
TENANT_ID = "<YOUR_TENANT_ID>"
SCOPE = "https://graph.microsoft.com/.default"
GRANT_TYPE = "client_credentials"


# Get Access Token
def get_access_token(tenant_id: str) -> str:
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPE,
        "grant_type": GRANT_TYPE,
    }

    response = requests.post(token_url, data=payload)

    if response.status_code != 200:
        print("Failed to get token:", response.status_code, response.text)
        return None

    token_json = response.json()
    return token_json.get("access_token")


#Get Meeting Response
def get_meeting_response(access_token: str, upn: str, start_time: str, end_time: str, subject: str):
    url = f"https://graph.microsoft.com/v1.0/users/{upn}/onlineMeetings"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "startDateTime": start_time,
        "endDateTime": end_time,
        "subject": subject
    }

    response = requests.post(url, headers=headers, json=payload)

    return response


#Create Teams Online Meeting
def create_meeting(upn: str, start_time: str, end_time: str, subject: str):
    token = get_access_token(TENANT_ID)
    if not token:
        return {
            "success": False,
            "message": "Could not obtain access token",
            "join_url": None,
            "raw_response": None,
        }

    response = get_meeting_response(token, upn, start_time, end_time, subject)

    if response.status_code in (200, 201):
        data = response.json()

        join_url = data.get("joinWebUrl")
        return {
            "success": True,
            "status_code": response.status_code,
            "join_url": join_url,
            "raw_response": data,
        }
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "message": "Failed to create online meeting",
            "raw_response": response.text,
        }


