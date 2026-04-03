# -*- coding: utf-8 -*-

"""
SwarmDigiz AI Auto-Optimization Engine
Continuously improves marketing performance.
"""

import sqlite3

DB_PATH = "swarmdigiz/swarmdigiz.db"


def analyze_performance(business_id):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # leads
    cur.execute(
        """
        SELECT COUNT(*)
        FROM inspection_runs
        WHERE business_id = ?
        """,
        (business_id,)
    )
    leads = cur.fetchone()[0] or 0

    # bookings
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

    # revenue
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

    conn.close()

    conversion = 0

    if leads > 0:
        conversion = bookings / leads

    return {
        "leads": leads,
        "bookings": bookings,
        "revenue": revenue,
        "conversion": conversion
    }


def recommend_strategy(metrics):

    conversion = metrics["conversion"]

    if conversion > 0.40:
        return {
            "strategy": "scale_budget",
            "message": "Increase campaign budget — high conversion detected."
        }

    elif conversion > 0.20:
        return {
            "strategy": "remarketing",
            "message": "Enable remarketing to capture undecided leads."
        }

    else:
        return {
            "strategy": "discount_campaign",
            "message": "Conversion low — push discount campaign."
        }


def run_auto_optimizer(business_id):

    metrics = analyze_performance(business_id)

    recommendation = recommend_strategy(metrics)

    return {
        "metrics": metrics,
        "recommendation": recommendation
    }