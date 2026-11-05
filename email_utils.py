import os
import requests

def send_email(to_email, subject, message):
    api_key = os.getenv("RESEND_API_KEY")

    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "from": "Lead Automation <onboarding@resend.dev>",
            "to": [to_email],
            "subject": subject,
            "text": message
        }
    )

    response.raise_for_status()