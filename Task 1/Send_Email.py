import smtplib
from email.mime.text import MIMEText
import re

def extract_email_details(text):
        subject_search = re.search(r'subject (.*?)( body| recipient|$)', text, re.IGNORECASE)
        body_search = re.search(r'body (.*?)( subject| recipient|$)', text, re.IGNORECASE)
        recipient_search = re.search(r'recipient (.*?)( subject| body|$)', text, re.IGNORECASE)

        subject = subject_search.group(1).strip() if subject_search else "No Subject"
        body = body_search.group(1).strip() if body_search else "No Body"
        recipient = recipient_search.group(1).strip() if recipient_search else "recipient@example.com"

        return subject, body, recipient

def send_email(subject, body, to_email):
        from_email = "your_email@example.com"
        password = "your_password"  # Consider using environment variables for security

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                        server.login(from_email, password)
                        server.sendmail(from_email, to_email, msg.as_string())
                return "Email sent successfully."
        except Exception as e:
                return f"Failed to send email: {e}"