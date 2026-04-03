def generate_visual_quote(inspection_result):

    estimated_total = inspection_result.get("estimated_total", 0)
    job_score = inspection_result.get("job_score", 0)
    tier = inspection_result.get("value_tier", "standard")

    discount = 0
    urgency = "normal"
    upsell = None

    # ==========================================
    # DISCOUNT ENGINE
    # ==========================================

    if tier == "premium":
        discount = 0
        urgency = "high"

    elif tier == "high":
        discount = 5
        urgency = "high"

    elif tier == "standard":
        discount = 10

    elif tier == "low":
        discount = 15

    quote_price = round(estimated_total * (1 - discount / 100), 2)

    # ==========================================
    # UPSELL ENGINE
    # ==========================================

    services = inspection_result.get("services_detected", [])

    if "air_duct_cleaning" in services:
        upsell = "Dryer Vent Cleaning Add-On $49"

    elif "carpet_cleaning" in services:
        upsell = "3 Room Deodorizer $39"

    # ==========================================
    # FINAL STRUCTURE
    # ==========================================

    return {
        "quote_price": quote_price,
        "discount_applied": discount,
        "urgency": urgency,
        "upsell_offer": upsell,
        "cta": "Book Now",
    }