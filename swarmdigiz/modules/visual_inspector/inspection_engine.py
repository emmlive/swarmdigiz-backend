# =========================================================
# AIR DUCT
# =========================================================
def evaluate_air_duct(data, config):
    vent_count = data.get("vent_count", 0)

    if vent_count >= 20:
        tier = "premium"
    elif vent_count >= 10:
        tier = "high"
    elif vent_count > 0:
        tier = "standard"
    else:
        tier = "low"

    estimated = vent_count * config.get("price_per_vent", 25)

    return {
        "service": "air_duct_cleaning",
        "vent_count": vent_count,
        "estimated_total": estimated,
        "tier": tier
    }


# =========================================================
# DRYER VENT
# =========================================================
def evaluate_dryer_vent(data, config):
    years = data.get("years_since_cleaning", 0)

    if years >= 5:
        tier = "high"
    elif years >= 2:
        tier = "standard"
    else:
        tier = "low"

    estimated = config.get("base_price", 120)

    return {
        "service": "dryer_vent_cleaning",
        "years_since_cleaning": years,
        "estimated_total": estimated,
        "tier": tier
    }


# =========================================================
# CARPET
# =========================================================
def evaluate_carpet(data, config):
    room_count = data.get("room_count", 0)

    if room_count >= 5:
        tier = "premium"
    elif room_count >= 3:
        tier = "high"
    elif room_count > 0:
        tier = "standard"
    else:
        tier = "low"

    estimated = room_count * config.get("price_per_room", 60)

    return {
        "service": "carpet_cleaning",
        "room_count": room_count,
        "estimated_total": estimated,
        "tier": tier
    }


# =========================================================
# HVAC
# =========================================================
def evaluate_hvac(data, config):
    service_type = data.get("service_type", "maintenance")
    emergency = data.get("emergency", False)

    if service_type == "installation":
        tier = "premium"
    elif service_type == "repair":
        tier = "high"
    else:
        tier = "standard"

    if emergency:
        tier = "premium"

    estimated = config.get("base_price", 250)

    return {
        "service": "hvac_service",
        "service_type": service_type,
        "emergency": emergency,
        "estimated_total": estimated,
        "tier": tier
    }