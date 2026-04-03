# -*- coding: utf-8 -*-

"""
SwarmDigiz Growth Metrics Engine
Aggregates AI-driven business intelligence
for the Growth Command Center.
"""

import json
from core.db import get_connection


# =========================================================
# GLOBAL GROWTH METRICS
# =========================================================

def get_growth_metrics(business_id):

    conn = get_connection()
    cur = conn.cursor()

    # Total inspections
    cur.execute(
        """
        SELECT COUNT(*)
        FROM inspection_runs
        WHERE business_id = ?
        """,
        (business_id,)
    )

    total_inspections = cur.fetchone()[0]

    # Estimated revenue
    cur.execute(
        """
        SELECT payload
        FROM inspection_runs
        WHERE business_id = ?
        """,
        (business_id,)
    )

    rows = cur.fetchall()

    estimated_revenue = 0
    lead_scores = []

    for r in rows:

        payload = json.loads(r[0])

        estimated_revenue += payload.get("estimated_price", 0)
        lead_scores.append(payload.get("lead_score", 0))

    avg_lead_score = 0

    if lead_scores:
        avg_lead_score = sum(lead_scores) / len(lead_scores)

    conn.close()

    return {
        "total_inspections": total_inspections,
        "estimated_revenue": estimated_revenue,
        "avg_lead_score": round(avg_lead_score, 2)
    }


# =========================================================
# LEAD TIER DISTRIBUTION
# =========================================================

def get_lead_tier_distribution(business_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT payload
        FROM inspection_runs
        WHERE business_id = ?
        """,
        (business_id,)
    )

    rows = cur.fetchall()

    tiers = {
        "hot": 0,
        "warm": 0,
        "cold": 0
    }

    for r in rows:

        payload = json.loads(r[0])
        tier = payload.get("lead_tier")

        if tier in tiers:
            tiers[tier] += 1

    conn.close()

    return tiers


# =========================================================
# CAMPAIGN PERFORMANCE
# =========================================================

def get_campaign_performance(business_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM swarm_runs
        WHERE business_id = ?
        """,
        (business_id,)
    )

    campaigns_launched = cur.fetchone()[0]

    conn.close()

    return {
        "campaigns_launched": campaigns_launched
    }