def calculate_lead_score(inspection_data: dict) -> dict:
    """
    Generic Lead Intelligence Engine

    Scores a lead using service-agnostic signals so SwarmDigiz
    can work across multiple local business categories.

    Expected inspection_data keys (optional/flexible):
    - severity: str
    - urgency: str
    - estimated_value: int | float
    - confidence: int | float
    - issue_detected: bool
    - booked: bool
    - service_type: str
    """

    severity = (inspection_data.get("severity") or "low").lower()
    urgency = (inspection_data.get("urgency") or "low").lower()
    estimated_value = inspection_data.get("estimated_value") or 0
    confidence = inspection_data.get("confidence") or 0
    issue_detected = bool(inspection_data.get("issue_detected", False))
    booked = bool(inspection_data.get("booked", False))
    service_type = inspection_data.get("service_type") or "general"

    score = 0
    reasons = []

    # Severity
    severity_points = {
        "low": 10,
        "medium": 25,
        "high": 40,
        "critical": 50,
    }
    sev_score = severity_points.get(severity, 10)
    score += sev_score
    reasons.append(f"Severity: {severity} (+{sev_score})")

    # Urgency
    urgency_points = {
        "low": 5,
        "medium": 15,
        "high": 25,
        "emergency": 35,
    }
    urg_score = urgency_points.get(urgency, 5)
    score += urg_score
    reasons.append(f"Urgency: {urgency} (+{urg_score})")

    # Estimated job value
    if estimated_value >= 500:
        score += 20
        reasons.append("High estimated job value (+20)")
    elif estimated_value >= 200:
        score += 12
        reasons.append("Medium estimated job value (+12)")
    elif estimated_value > 0:
        score += 6
        reasons.append("Low estimated job value (+6)")

    # AI / inspection confidence
    if confidence >= 90:
        score += 15
        reasons.append("Very high detection confidence (+15)")
    elif confidence >= 75:
        score += 10
        reasons.append("High detection confidence (+10)")
    elif confidence >= 50:
        score += 5
        reasons.append("Moderate detection confidence (+5)")

    # Problem detected
    if issue_detected:
        score += 15
        reasons.append("Issue detected (+15)")

    # Already booked = hot lead / conversion-ready
    if booked:
        score += 20
        reasons.append("Customer already booked (+20)")

    # Cap score at 100
    score = min(score, 100)

    # Tiering
    if score >= 80:
        tier = "HIGH"
        recommended_action = [
            "Launch paid ads",
            "Prioritize immediate follow-up",
            "Send booking reminder",
        ]
    elif score >= 50:
        tier = "MEDIUM"
        recommended_action = [
            "Retarget with offer",
            "Send nurture follow-up",
        ]
    else:
        tier = "LOW"
        recommended_action = [
            "Add to nurture sequence",
            "Monitor for future remarketing",
        ]

    return {
        "service_type": service_type,
        "lead_score": score,
        "lead_tier": tier,
        "recommended_action": recommended_action,
        "reasons": reasons,
    }