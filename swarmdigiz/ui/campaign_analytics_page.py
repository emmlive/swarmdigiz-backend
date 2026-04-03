import streamlit as st
import sqlite3


DB_PATH = "swarmdigiz/swarmdigiz.db"


def load_campaign_stats(business_id):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Total campaigns launched
    cur.execute("""
        SELECT connector_type, COUNT(*)
        FROM connector_logs
        WHERE business_id = ?
        GROUP BY connector_type
    """, (business_id,))

    campaigns = cur.fetchall()

    # Leads generated
    cur.execute("""
        SELECT COUNT(*)
        FROM inspection_runs
        WHERE business_id = ?
    """, (business_id,))

    leads = cur.fetchone()[0]

    # Estimated revenue
    cur.execute("""
        SELECT SUM(estimated_quote)
        FROM inspection_runs
        WHERE business_id = ?
    """, (business_id,))

    revenue = cur.fetchone()[0] or 0

    conn.close()

    return campaigns, leads, revenue


def render_campaign_analytics(business_id: int):

    st.title("📈 Campaign Analytics")

    campaigns, leads, revenue = load_campaign_stats(business_id)

    # Top metrics
    c1, c2, c3 = st.columns(3)

    total_campaigns = sum([c[1] for c in campaigns]) if campaigns else 0

    c1.metric("Campaigns Launched", total_campaigns)
    c2.metric("Leads Generated", leads)
    c3.metric("Estimated Revenue", f"${revenue}")

    st.markdown("---")

    st.markdown("### Platform Breakdown")

    if not campaigns:
        st.info("No campaigns launched yet.")
        return

    for platform, count in campaigns:

        with st.container():

            p1, p2 = st.columns(2)

            p1.write(f"**{platform.replace('_', ' ').title()}**")
            p2.write(f"{count} campaigns")

            st.markdown("---")