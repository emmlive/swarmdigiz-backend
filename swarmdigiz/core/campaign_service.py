def build_campaign_from_swarm(business_name: str, swarm_outputs: dict):
    """
    Convert swarm agent outputs into a structured campaign
    that can be edited or deployed to ad platforms.
    """

    ad_copy = swarm_outputs.get("Ad Copy Agent", "")
    landing = swarm_outputs.get("Landing Page Architect", "")
    funnel = swarm_outputs.get("Funnel Strategist", "")

    campaign = {
        "business_name": business_name,
        "google_ads": {
            "headline": "Fast, Reliable Service – Done Right.",
            "description": "Call today for immediate service.",
            "keywords": [
                f"{business_name.lower()} service",
                f"{business_name.lower()} near me",
                "local service company"
            ]
        },
        "facebook_ads": {
            "primary_text": ad_copy[:200] if ad_copy else "Need reliable local service? Book today for fast, professional help.",
            "headline": "Book Your Service Today",
            "cta": "BOOK_NOW"
        },
        "landing_page": {
            "structure": landing,
            "funnel": funnel
        }
    }

    return campaign


def build_campaign_from_lead(
    business_name: str,
    service_type: str,
    lead_tier: str,
    lead_score: int,
    quote_total: float | int = 0
):
    """
    Generic campaign generator from lead intelligence.
    Service-agnostic by design.
    """

    readable_service = service_type.replace("_", " ").title() if service_type else "Local Service"

    urgency_line = "High-priority service available now." if lead_tier == "HIGH" else "Professional local service available."

    value_line = f"Est. service value from inspection: ${quote_total}." if quote_total else "Fast response available."

    google_headline = f"{readable_service} Near You"
    google_description = f"{urgency_line} Book trusted {readable_service.lower()} today. {value_line}"

    facebook_primary = (
        f"We detected a strong {readable_service.lower()} opportunity. "
        f"Lead score: {lead_score}. {urgency_line} Book now."
    )

    campaign = {
        "business_name": business_name,
        "source": "lead_intelligence",
        "google_ads": {
            "headline": google_headline[:30],
            "description": google_description[:90],
            "keywords": [
                f"{readable_service.lower()} near me",
                f"{readable_service.lower()} service",
                f"best {readable_service.lower()} company",
            ]
        },
        "facebook_ads": {
            "headline": f"Book {readable_service} Today",
            "primary_text": facebook_primary[:220],
            "cta": "BOOK_NOW"
        },
        "meta": {
            "service_type": service_type,
            "lead_tier": lead_tier,
            "lead_score": lead_score,
            "quote_total": quote_total,
        }
    }

    return campaign