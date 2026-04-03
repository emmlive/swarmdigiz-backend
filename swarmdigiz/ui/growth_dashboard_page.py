# -*- coding: utf-8 -*-

import streamlit as st
import sqlite3
import json

from core.ai_auto_optimizer import run_auto_optimizer

DB_PATH = "swarmdigiz/swarmdigiz.db"


# =========================================================
# CORE METRICS
# =========================================================

def get_growth_metrics(business_id):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Total leads
    try:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM inspection_runs
            WHERE business_id = ?
            """,
            (business_id,)
        )
        total_leads = cur.fetchone()[0] or 0
    except:
        total_leads = 0

    # Estimated revenue
    try:
        cur.execute(
            """
            SELECT SUM(estimated_revenue)
            FROM inspection_runs
            WHERE business_id = ?
            """,
            (business_id,)
        )
        revenue = cur.fetchone()[0] or 0
    except:
        revenue = 0

    # Average lead score
    try:
        cur.execute(
            """
            SELECT AVG(lead_score)
            FROM inspection_runs
            WHERE business_id = ?
            """,
            (business_id,)
        )
        avg_score = cur.fetchone()[0] or 0
    except:
        avg_score = 0

    # Bookings
    try:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE business_id = ?
            """,
            (business_id,)
        )
        bookings = cur.fetchone()[0] or 0
    except:
        bookings = 0

    conn.close()

    conversion = 0
    if total_leads > 0:
        conversion = round((bookings / total_leads) * 100, 1)

    return {
        "leads": total_leads,
        "revenue": revenue,
        "avg_score": round(avg_score, 1),
        "bookings": bookings,
        "conversion": conversion,
    }


# =========================================================
# LEAD TIER DISTRIBUTION
# =========================================================

def get_lead_tiers(business_id):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    tiers = {
        "hot": 0,
        "warm": 0,
        "cold": 0
    }

    try:
        cur.execute(
            """
            SELECT payload
            FROM inspection_runs
            WHERE business_id = ?
            """,
            (business_id,)
        )

        rows = cur.fetchall()

        for r in rows:

            try:
                payload = json.loads(r[0])
                tier = payload.get("lead_tier")

                if tier in tiers:
                    tiers[tier] += 1
            except:
                continue

    except:
        pass

    conn.close()

    return tiers


# =========================================================
# CAMPAIGN PERFORMANCE
# =========================================================

def get_campaign_stats(business_id):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM swarm_runs
            WHERE business_id = ?
            """,
            (business_id,)
        )

        campaigns = cur.fetchone()[0] or 0

    except:
        campaigns = 0

    conn.close()

    return campaigns


# =========================================================
# DASHBOARD UI
# =========================================================

def render_growth_dashboard(business_id):

    st.title("📈 AI Growth Command Center")

    metrics = get_growth_metrics(business_id)

    col1, col2, col3 = st.columns(3)

    col1.metric("Leads Captured", metrics["leads"])
    col2.metric("Bookings", metrics["bookings"])
    col3.metric("Conversion Rate", f"{metrics['conversion']}%")

    st.markdown("---")

    col4, col5 = st.columns(2)

    col4.metric("Estimated Revenue", f"${metrics['revenue']}")
    col5.metric("Average Lead Score", metrics["avg_score"])

    st.markdown("---")

    # =====================================================
    # Lead Tier Distribution
    # =====================================================

    st.subheader("Lead Intelligence")

    tiers = get_lead_tiers(business_id)

    st.bar_chart({
        "Hot Leads": tiers["hot"],
        "Warm Leads": tiers["warm"],
        "Cold Leads": tiers["cold"]
    })

    st.markdown("---")

    # =====================================================
    # Campaign Performance
    # =====================================================

    campaigns = get_campaign_stats(business_id)

    st.metric("Marketing Campaigns Launched", campaigns)

    st.markdown("---")

    # =====================================================
    # AI Auto Optimization Engine
    # =====================================================

    st.subheader("🤖 AI Optimization Recommendation")

    try:

        optimization = run_auto_optimizer(business_id)

        recommendation = optimization["recommendation"]["message"]

        st.info(recommendation)

    except:

        st.info("AI optimization engine initializing...")

    st.markdown("---")

    st.success(
        "SwarmDigiz AI is actively generating leads, optimizing campaigns, and increasing revenue."
    )