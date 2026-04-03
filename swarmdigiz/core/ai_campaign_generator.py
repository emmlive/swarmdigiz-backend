# -*- coding: utf-8 -*-

"""
SwarmDigiz AI Campaign Generator

Creates marketing assets from inspection + lead intelligence data.
"""

def generate_ai_campaign_assets(result):

    service = "your service"
    services = result.get("services", {})

    if services:
        service = list(services.keys())[0].replace("_", " ").title()

    lead_tier = result.get("lead_tier", "cold")

    # ---------------------------------------------------------
    # Google Ad
    # ---------------------------------------------------------

    google_ad = {
        "headline": f"{service} Near You",
        "description": f"Professional {service.lower()} services. Book today.",
        "cta": "Book Service",
    }

    # ---------------------------------------------------------
    # Facebook Ad
    # ---------------------------------------------------------

    facebook_ad = {
        "headline": f"Need {service}?",
        "text": f"Our experts provide fast and affordable {service.lower()}. Schedule your appointment today.",
        "cta": "Get Quote",
    }

    # ---------------------------------------------------------
    # Landing Page Copy
    # ---------------------------------------------------------

    landing_page = {
        "title": f"Professional {service}",
        "subtitle": "Fast, Affordable, Trusted Service",
        "body": f"We provide high-quality {service.lower()} services with experienced technicians. Get your quote today and schedule your service in minutes.",
    }

    # ---------------------------------------------------------
    # Email Follow-up
    # ---------------------------------------------------------

    email_followup = {
        "subject": f"Your {service} Quote",
        "body": f"Thank you for your interest in our {service.lower()} service. Our team is ready to assist you. Click below to book your appointment today.",
    }

    return {
        "google_ad": google_ad,
        "facebook_ad": facebook_ad,
        "landing_page": landing_page,
        "email_followup": email_followup,
        "lead_tier": lead_tier,
    }