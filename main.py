import os
import requests
import time
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
BOOTDEV_PROFILE = os.getenv("BOOTDEV_PROFILE")

NOTIFY_ADDRESS = os.getenv("NOTIFY_ADDRESS")
SENDING_ALIAS = os.getenv("SENDING_ALIAS")
SENDING_DOMAIN_NAME = os.getenv("SENDING_DOMAIN_NAME")

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_API_URL = "https://api.mailgun.net/v3/" + SENDING_DOMAIN_NAME + "/messages"

FROM_ADDRESS = SENDING_ALIAS + "@" + SENDING_DOMAIN_NAME

def get_completed_lessons():
    page = requests.get(BOOTDEV_PROFILE)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("span", class_="text-2xl font-bold text-white")
    return int(results.text)

def send_email(to_address: str, subject: str, message: str):
    try:
        resp = requests.post(MAILGUN_API_URL, auth=("api", MAILGUN_API_KEY),
            data={
                "from": FROM_ADDRESS,
            "to": to_address,
            "subject": subject,
            "text": message
            })
        if resp.status_code == 200:
            print(f"Successfully sent an email to '{to_address}' via Mailgun API.")
        else:
            print(f"Could not send the email, reason: {resp.text}")

    except Exception as ex:
        print(f"Mailgun error: {ex}")

def main():
    last_completed_lessons = get_completed_lessons()
    hours_since_last_completed = 0
    send_email(NOTIFY_ADDRESS, "Study Buddy Started", "The study buddy has been stated. This will notify if lessons have been completed in the past hour, if no lessons have been completed for the past 8 hours, and if no lessons have been completed for over 18 hours.")
    while True:
        completed_lessons = get_completed_lessons()
        diff = completed_lessons - last_completed_lessons
        print(f"{diff} lessons have been completed in the last hour.")
        if diff > 0:
            hours_since_last_completed = 0
            send_email(NOTIFY_ADDRESS, f"{diff} lessons completed in the past hour.", f"{diff} lessons were completed in the past hour!")
        else:
            hours_since_last_completed = hours_since_last_completed + 1
            if hours_since_last_completed % 8 == 0:
                send_email(NOTIFY_ADDRESS, f"0 lessons have been completed in the past {hours_since_last_completed} hours.", f"{diff} were completed in the past hour. :(")
            elif hours_since_last_completed % 18 == 0:
                print(f"It has been {hours_since_last_completed} hours since the last lesson was completed.")
        last_completed_lessons = completed_lessons
        time.sleep(3600)

if __name__ == "__main__":
    main()