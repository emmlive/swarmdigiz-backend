import streamlit as st

from core.campaign_service import build_campaign_from_swarm
from connectors.facebook_ads_connector import FacebookAdsConnector
from connectors.google_ads_connector import GoogleAdsConnector


def render_campaign_builder(username, business_id):

    st.title("📢 Campaign Builder")

    swarm_results = st.session_state.get("__last_swarm_results__")
    campaign_draft = st.session_state.get("__last_campaign_draft__")

    if not swarm_results and not campaign_draft:
        st.warning("Run the Marketing Swarm or Visual Inspector first to generate campaign content.")
        return

    business_name = st.session_state.get("business_name", "My Business")

    # Priority 1: use campaign draft generated from Visual Inspector / Lead Engine
    if campaign_draft:
        campaign = campaign_draft
    else:
        campaign = build_campaign_from_swarm(business_name, swarm_results)

    st.markdown("### Google Ads Campaign")

    headline = st.text_input(
        "Headline",
        campaign["google_ads"]["headline"]
    )

    description = st.text_area(
        "Description",
        campaign["google_ads"]["description"]
    )

    keywords = st.text_area(
        "Keywords (one per line)",
        "\n".join(campaign["google_ads"].get("keywords", []))
    )

    st.markdown("### Facebook Ad")

    fb_headline = st.text_input(
        "Facebook Headline",
        campaign["facebook_ads"].get("headline", "Book Your Service Today")
    )

    primary_text = st.text_area(
        "Primary Text",
        campaign["facebook_ads"]["primary_text"]
    )

    cta = st.selectbox(
        "Facebook CTA",
        ["BOOK_NOW", "LEARN_MORE", "CALL_NOW"],
        index=["BOOK_NOW", "LEARN_MORE", "CALL_NOW"].index(
            campaign["facebook_ads"].get("cta", "BOOK_NOW")
        ) if campaign["facebook_ads"].get("cta", "BOOK_NOW") in ["BOOK_NOW", "LEARN_MORE", "CALL_NOW"] else 0
    )

    st.markdown("---")

    if st.button("🚀 Deploy Campaign"):

        google_payload = {
            "headline": headline,
            "description": description,
            "keywords": [k.strip() for k in keywords.splitlines() if k.strip()]
        }

        facebook_payload = {
            "headline": fb_headline,
            "primary_text": primary_text,
            "cta": cta
        }

        google = GoogleAdsConnector().execute(google_payload)
        facebook = FacebookAdsConnector().execute(facebook_payload)

        st.success("Campaign deployed successfully")

        st.json({
            "google": google,
            "facebook": facebook
        })