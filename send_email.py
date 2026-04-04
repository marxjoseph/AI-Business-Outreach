import smtplib
import os
from dotenv import load_dotenv
from openai import OpenAI
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY"))

response = client.responses.create(
    model="gpt-5.4-mini",
    input="Write a few sentences on the moon landing"
)

# Example usage
body = response.output_text

print(body)

# Your email credentials
EMAIL = "marquesjoseph03@gmail.com"
PASSWORD = os.getenv("PASSWORD")

# Receiver
to_email = "josephmarques@cmail.carleton.ca"

# Create the email
msg = MIMEMultipart()
msg["From"] = EMAIL
msg["To"] = to_email
msg["Subject"] = "Hello from my script"

msg.attach(MIMEText(body, "plain"))

# Send the email
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Secure connection
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print("Error:", e)