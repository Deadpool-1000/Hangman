import os

import requests
from dotenv import load_dotenv

load_dotenv()


def send_simple_message():
    return (
        requests.post(
            "https://api.mailgun.net/v3/sandboxca4f9e9c2e5949d7b88a48a1c8561d32.mailgun.org/messages",
            auth=("api", os.getenv("MAILGUN_API_KEY")),
            data={
                "from": "Milind@sandboxca4f9e9c2e5949d7b88a48a1c8561d32.mailgun.org",
                "to": ["milibhatnagar2002@gmail.com"],
                "subject": "Test email",
                "text": "This is a test email."
            }
        )
    )


send_simple_message()
