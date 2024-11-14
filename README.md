# Boot.Dev Study Buddy
This is a basic script that sends an emails about study progress, using the lessons completed on you Boot.Dev profile. This can encourage productivity, or you can have the notifcations go to someone else who is holding you accountable.

Emails are sent using the Mailgun API. Be sure that you have setup your domain with Mailgun, and have an API key for that domain.

# Setup

Clone the repo
```
git clone https://github.com/Rodabaugh/boot-dev-studybuddy
```

Install dependencies
```
pip install python-dotenv beautifulsoup4
```

Create a .env file in the same folder as the main.py. It should look like the one below.
```
BOOTDEV_PROFILE=(URL to Boot.Dev Profile to Monitor)

NOTIFY_ADDRESS=(The address you want to send notifcations to)
SENDING_ALIAS=(The alias for the email address to send as)
SENDING_DOMAIN_NAME=(The domain you want to send emails from)

MAILGUN_API_KEY=(Your Mailgun API Key, approved to send for your sending domain)
```

Run the script
```
python main.py
```
