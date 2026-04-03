# swarmdigiz/modules/visual_inspector/marketing_signal_engine.py


def build_marketing_signals(total_value, job_score, value_tier, services_selected):
    """
    Creates structured marketing alignment signals
    for Google Ads, Facebook, automation routing, and SaaS analytics.
    """

    # Google & Facebook conversion value alignment
    google_conversion_value = total_value
    facebook_event_value = total_value

    # Retargeting bucket logic
    if value_tier == "premium":
        retargeting_bucket = "premium_home_service"
    elif value_tier == "high":
        retargeting_bucket = "high_value_service"
    elif value_tier == "standard":
        retargeting_bucket = "standard_service"
    else:
        retargeting_bucket = "low_value_service"

    # Priority routing logic
    priority_flag = job_score >= 75

    # Emergency detection
    emergency_flag = False
    if "hvac_service" in services_selected:
        # emergency detection expected to be handled upstream
        # but we leave room for automation tagging
        emergency_flag = True if job_score >= 85 else False

    return {
        "google_conversion_value": google_conversion_value,
        "facebook_event_value": facebook_event_value,
        "retargeting_bucket": retargeting_bucket,
        "priority_flag": priority_flag,
        "emergency_flag": emergency_flag
    }