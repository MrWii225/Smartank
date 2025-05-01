import smtplib
from email.message import EmailMessage
import json

with open('settings.json', 'r') as settings:
    data=json.load(settings)
    num = data.get("phone_number")
    provider = data.get("provider")

# need a way to set message based on what the notification should be. Probably should do functions on GUI
def set_message():
    return "BABABA"
msg = EmailMessage()
msg.set_content(f"{set_message()}")
msg["Subject"] = "SMARTANK"
msg["From"] = "smartank100@gmail.com"
msg["To"] = f"{num}@{provider}" # One bracket will house the number the user inputs and the other will include the
# suffix needed at the end for each provider "vtext.com", "txt.att.net", "tmomail.net", "messaging.sprintpcs.com"

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login("smartank100@gmail.com", "cnae ccjt hyat qfti")
    smtp.send_message(msg)
