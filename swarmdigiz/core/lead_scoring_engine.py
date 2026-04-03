def calculate_lead_score(payload):
    """
    AI Lead Scoring Engine

    Evaluates inspection payload and produces:
    - lead_score (0-100)
    - lead_tier
    - marketing_priority
    """

    score = 0

    # -------------------------------------------------
    # SERVICE VALUE WEIGHT
    # -------------------------------------------------

    services = payload.get("services", {})

    if "air_duct_cleaning" in services:
        vents = services["air_duct_cleaning"].get("vent_count", 0)
        score += min(vents * 2, 30)

    if "dryer_vent_cleaning" in services:
        years = services["dryer_vent_cleaning"].get("years_since_cleaning", 0)
        score += min(years * 3, 25)

    if "carpet_cleaning" in services:
        rooms = services["carpet_cleaning"].get("room_count", 0)
        score += min(rooms * 3, 30)

    if "hvac_service" in services:
        service_type = services["hvac_service"].get("service_type")

        if service_type == "installation":
            score += 40
        elif service_type == "repair":
            score += 25
        else:
            score += 10

    # -------------------------------------------------
    # AI SEVERITY BONUS
    # -------------------------------------------------

    severity = payload.get("ai_severity")

    if severity:
        score += severity * 2

    # -------------------------------------------------
    # EMERGENCY SIGNAL
    # -------------------------------------------------

    hvac = services.get("hvac_service")

    if hvac and hvac.get("emergency"):
        score += 25

    # -------------------------------------------------
    # CAP SCORE
    # -------------------------------------------------

    score = min(score, 100)

    # -------------------------------------------------
    # LEAD TIER CLASSIFICATION
    # -------------------------------------------------

    if score >= 75:
        tier = "hot"
        marketing_priority = "high"

    elif score >= 45:
        tier = "warm"
        marketing_priority = "medium"

    else:
        tier = "cold"
        marketing_priority = "low"

    return {
        "lead_score": score,
        "lead_tier": tier,
        "marketing_priority": marketing_priority
    }