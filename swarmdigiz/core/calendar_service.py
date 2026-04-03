# core/calendar_service.py

from datetime import datetime, timedelta


# =========================================================
# GENERATE TIME SLOTS
# =========================================================

def generate_time_slots(
    start_hour=9,
    end_hour=17,
    interval_minutes=120
):
    """
    Generate time slots for a day.
    Default: 9AM–5PM in 2-hour intervals.
    """

    slots = []

    current = datetime.now().replace(
        hour=start_hour,
        minute=0,
        second=0,
        microsecond=0
    )

    end = current.replace(hour=end_hour)

    while current <= end:
        slots.append(current.strftime("%I:%M %p"))
        current += timedelta(minutes=interval_minutes)

    return slots


# =========================================================
# VALIDATE DATE
# =========================================================

def is_valid_date(selected_date):
    """
    Ensure date is today or future.
    """
    if not selected_date:
        return False

    today = datetime.today().date()
    return selected_date >= today


# =========================================================
# FORMAT APPOINTMENT
# =========================================================

def format_appointment(date, time):
    """
    Combine date + time into a single string.
    """
    if not date or not time:
        return None

    return f"{date} {time}"