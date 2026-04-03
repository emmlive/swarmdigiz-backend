# -*- coding: utf-8 -*-

"""
SwarmDigiz Customer Notification Engine
Handles SMS and Email notifications for leads.
"""


def send_sms_notification(phone, message):

    # placeholder for Twilio / SMS provider
    return {
        "status": "sent",
        "channel": "sms",
        "phone": phone,
        "message": message
    }


def send_email_notification(email, subject, body):

    # placeholder for email provider
    return {
        "status": "sent",
        "channel": "email",
        "email": email,
        "subject": subject
    }


def send_quote_notifications(customer, quote):

    phone = customer.get("phone")
    email = customer.get("email")

    sms_message = f"Your quote is ${quote['total']}. Book your service today."

    email_subject = "Your Service Quote"
    email_body = f"""
Hello,

Your quote is ${quote['total']}.

Click below to schedule your service.

Thank you.
"""

    responses = {}

    if phone:
        responses["sms"] = send_sms_notification(phone, sms_message)

    if email:
        responses["email"] = send_email_notification(email, email_subject, email_body)

    return responses