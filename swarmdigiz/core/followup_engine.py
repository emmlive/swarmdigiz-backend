# -*- coding: utf-8 -*-

"""
SwarmDigiz Follow-Up Engine

Handles automated reminders after quote generation.

Features:
- Follow-up scheduling
- SMS + Email reminders
- Automation Guard protection
"""

from datetime import datetime, timedelta

from core.notification_engine import send_sms_notification, send_email_notification
from core.automation_guard import allow


# ---------------------------------------------------------
# BUILD FOLLOW-UP SCHEDULE
# ---------------------------------------------------------

def build_followup_schedule():

    now = datetime.utcnow()

    return [
        ("day1", now + timedelta(days=1)),
        ("day3", now + timedelta(days=3)),
        ("day7", now + timedelta(days=7)),
    ]


# ---------------------------------------------------------
# SEND FOLLOW-UP MESSAGE
# ---------------------------------------------------------

def send_followup(customer, quote, stage):

    identifier = (
        customer.get("email")
        or customer.get("phone")
        or customer.get("name")
        or "unknown"
    )

    # Prevent duplicate follow-up sends
    if not allow(f"followup_send_{stage}", identifier):
        return {
            "status": "blocked",
            "reason": "duplicate follow-up prevented"
        }

    price = quote.get("total", 0)

    if stage == "day1":

        message = f"""
Reminder: Your service quote is still available.

Estimated price: ${price}

Book your appointment today.
"""

    elif stage == "day3":

        message = f"""
Limited Offer: Book your service now and receive a special discount.

Your estimate: ${price}
"""

    else:

        message = f"""
Final Reminder

Your quote of ${price} will expire soon.

Schedule today to secure your service.
"""

    results = {
        "sms": None,
        "email": None
    }

    if customer.get("phone"):
        results["sms"] = send_sms_notification(customer["phone"], message)

    if customer.get("email"):
        results["email"] = send_email_notification(
            customer["email"],
            "Service Quote Reminder",
            message
        )

    return {
        "status": "sent",
        "stage": stage,
        "results": results
    }


# ---------------------------------------------------------
# TRIGGER FOLLOW-UP SCHEDULE
# ---------------------------------------------------------

def trigger_followups(customer, quote):

    identifier = (
        customer.get("email")
        or customer.get("phone")
        or customer.get("name")
        or "unknown"
    )

    # Prevent duplicate follow-up schedule creation
    if not allow("followup_schedule", identifier):
        return []

    schedule = build_followup_schedule()

    results = []

    for stage, scheduled_time in schedule:

        results.append({
            "stage": stage,
            "scheduled_for": scheduled_time.isoformat()
        })

    return results