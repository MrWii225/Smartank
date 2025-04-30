import smtplib
from email.message import EmailMessage

def set_message():
    return "BABABA"
msg = EmailMessage()
msg.set_content(f"{set_message()}")
msg["Subject"] = "SMARTANK"
msg["From"] = "smartank100@gmail.com"
msg["To"] = "{}+{}"  # Verizon number

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login("smartank100@gmail.com", "cnae ccjt hyat qfti")
    smtp.send_message(msg)
