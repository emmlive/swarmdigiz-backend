# -*- coding: utf-8 -*-

"""
SwarmDigiz Notification Engine

Handles:
- Email notifications
- SMS notifications
- Quote delivery to customers

Includes Automation Guard protection to prevent
duplicate notifications.
"""

import smtplib
from email.mime.text import MIMEText

from core.automation_guard import allow


# ---------------------------------------------------------
# EMAIL NOTIFICATION
# ---------------------------------------------------------

def send_email_notification(to_email, subject, message):

    # Placeholder SMTP config (replace with environment variables later)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "your@email.com"
    smtp_password = "yourpassword"

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email

    try:

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)

        server.sendmail(smtp_user, [to_email], msg.as_string())

        server.quit()

        return True

    except Exception as e:

        return {
            "status": "email_failed",
            "error": str(e)
        }


# ---------------------------------------------------------
# SMS NOTIFICATION (Twilio placeholder)
# ---------------------------------------------------------

def send_sms_notification(phone, message):

    try:

        # Placeholder for Twilio integration
        print("SMS SENT TO:", phone)
        print(message)

        return True

    except Exception as e:

        return {
            "status": "sms_failed",
            "error": str(e)
        }


# ---------------------------------------------------------
# SEND QUOTE TO CUSTOMER
# ---------------------------------------------------------

def send_quote_notifications(customer, quote):

    identifier = (
        customer.get("email")
        or customer.get("phone")
        or customer.get("name")
        or "unknown"
    )

    # -----------------------------------------------------
    # Automation Guard Protection
    # -----------------------------------------------------

    if not allow("notification", identifier):

        return {
            "status": "blocked",
            "reason": "duplicate notification prevented"
        }

    message = f"""
Your service estimate is ready.

Estimated Price: ${quote.get('total', 0)}

Thank you for using our inspection tool.
"""

    results = {
        "email": None,
        "sms": None
    }

    # -----------------------------------------------------
    # Email Notification
    # -----------------------------------------------------

    if customer.get("email"):

        results["email"] = send_email_notification(
            customer["email"],
            "Your Service Quote",
            message
        )

    # -----------------------------------------------------
    # SMS Notification
    # -----------------------------------------------------

    if customer.get("phone"):

        results["sms"] = send_sms_notification(
            customer["phone"],
            message
        )

    return {
        "status": "sent",
        "results": results
    }