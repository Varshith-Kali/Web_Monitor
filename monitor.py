import time
import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuration
URL = os.getenv("URL")
KEYWORDS = ["IDFC", "IDFC First Bank", "IDFC Bank"]
# KEYWORDS = ["Federal Bank"]
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL"))  
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
RECIPIENT = os.getenv("RECIPIENT")

def check_for_keywords(url, keywords):
    """Fetch the page and check if any of the keywords exist in the target div."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            div = soup.find('div', class_='field-item even')
            if div:
                content = div.get_text(strip=True)
                for keyword in keywords:
                    if keyword in content:
                        return True
        return False
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return False

def send_email(subject, body):
    """Send an email with the given subject and body."""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = RECIPIENT
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            print("Alert email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def monitor_website():
    """Monitor the website and send an email alert if keywords are found."""
    print(f"Monitoring {URL} for keywords {KEYWORDS} every hour...")
    while True:
        if check_for_keywords(URL, KEYWORDS):
            subject = "Alert! IDFC-related Information Found"
            body = f"Alert! Some info related to IDFC has been added.\nClick here to check -> {URL}"
            send_email(subject, body)
        else:
            print("No keywords found.")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_website()
