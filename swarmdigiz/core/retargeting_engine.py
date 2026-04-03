# =========================================================
# RETARGETING SIGNAL ENGINE
# =========================================================

def generate_retargeting_signals(payload):
    """
    Convert inspection results into marketing retargeting signals.
    These signals help determine:
    - Lead priority
    - Upsell opportunity
    - Retargeting audience bucket
    - Ad platform value signals
    """

    estimated_total = payload.get("estimated_total", 0)
    job_score = payload.get("job_score", 0)
    value_tier = payload.get("value_tier", "low")

    # =====================================================
    # PRIORITY LEAD FLAG
    # =====================================================

    priority_lead = False

    if value_tier in ["premium", "high"]:
        priority_lead = True

    if job_score >= 70:
        priority_lead = True

    # =====================================================
    # UPSELL OPPORTUNITY
    # =====================================================

    upsell_opportunity = False

    if value_tier in ["standard", "low"]:
        upsell_opportunity = True

    # =====================================================
    # RETARGETING BUCKETS
    # =====================================================

    if estimated_total >= 700:
        audience_bucket = "premium_service"

    elif estimated_total >= 400:
        audience_bucket = "high_value_service"

    elif estimated_total >= 200:
        audience_bucket = "standard_service"

    else:
        audience_bucket = "low_value_service"

    # =====================================================
    # AD PLATFORM VALUE SIGNALS
    # =====================================================

    facebook_event_value = estimated_total
    google_conversion_value = estimated_total

    # =====================================================
    # BUILD SIGNAL PAYLOAD
    # =====================================================

    signals = {
        "priority_lead": priority_lead,
        "upsell_opportunity": upsell_opportunity,
        "audience_bucket": audience_bucket,
        "facebook_event_value": facebook_event_value,
        "google_conversion_value": google_conversion_value,
    }

    return signals