import requests

# ================= CONFIG =================
SENDGRID_API_KEY = "--"   
SENDER_EMAIL = "bhagyasrivaralakshmi@gmail.com"


# ================= EMAIL FUNCTION =================
def send_email(receiver_email, summary, actions, decisions):
    data = {
        "personalizations": [{
            "to": [{"email": receiver_email}],
            "subject": "Meeting Summary Report"
        }],
        "from": {"email": SENDER_EMAIL},
        "reply_to": {"email": SENDER_EMAIL},
        "content": [{
            "type": "text/plain",
            "value": f"""
Meeting Summary:

{summary}


Action Items:

{actions}


Decisions:

{decisions}
"""
        }]
    }

    response = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {SENDGRID_API_KEY}",
            "Content-Type": "application/json"
        },
        json=data
    )

    if response.status_code == 202:
        return "Email Sent Successfully ✅"
    else:
        return f"Error: {response.text}"
