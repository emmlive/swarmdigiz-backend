def generate_ai_upsells(result):
    """
    Generates smart upsell recommendations
    based on inspection signals.
    """

    upsells = []

    services = result.get("services", {})
    severity = result.get("ai_severity", 0)

    # -----------------------------------
    # AIR DUCT CLEANING
    # -----------------------------------
    if "air_duct_cleaning" in services:

        if severity >= 60:
            upsells.append({
                "service": "Sanitization Treatment",
                "price": 79
            })

            upsells.append({
                "service": "Mold Prevention Spray",
                "price": 129
            })

        upsells.append({
            "service": "Dryer Vent Cleaning",
            "price": 120
        })

    # -----------------------------------
    # DRYER VENT
    # -----------------------------------
    if "dryer_vent_cleaning" in services:

        upsells.append({
            "service": "Bird Guard Installation",
            "price": 65
        })

    # -----------------------------------
    # CARPET
    # -----------------------------------
    if "carpet_cleaning" in services:

        rooms = services["carpet_cleaning"].get("room_count", 0)

        if rooms >= 3:
            upsells.append({
                "service": "Carpet Protectant (Scotchgard)",
                "price": 45
            })

        upsells.append({
            "service": "Pet Odor Treatment",
            "price": 60
        })

    # -----------------------------------
    # HVAC
    # -----------------------------------
    if "hvac_service" in services:

        upsells.append({
            "service": "HVAC Filter Replacement",
            "price": 35
        })

        upsells.append({
            "service": "Annual Maintenance Plan",
            "price": 149
        })

    return upsells