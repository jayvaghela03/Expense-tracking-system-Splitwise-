import os
import requests

MAILGUN_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_URL = os.getenv("MAILGUN_API_URL")

def send_mail(subject,recipients,body):
    try:
        from_name= "example#gmail.com"
        recipient = recipients
        request_url = MAILGUN_URL

        response = requests.post(
            request_url,
            auth=("api", MAILGUN_KEY),
            data={
                "from": from_name, 
                "to": recipient, 
                "subject": subject,
                "html": body
            },
        )
        print(response.text)
    except Exception as e:
        print(e)
        raise 