import json
from datetime import datetime
from core.db import get_connection


# =========================================================
# CREATE INSPECTION RUN
# =========================================================

def create_inspection_run(username, payload, business_id):

    conn = get_connection()
    cur = conn.cursor()

    # Try to extract estimated revenue from payload safely
    estimated_revenue = 0

    try:
        estimated_revenue = payload.get("estimated_price") or payload.get("quote_total") or 0
    except Exception:
        estimated_revenue = 0

    cur.execute(
        """
        INSERT INTO inspection_runs
        (username, business_id, payload, estimated_revenue, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            username,
            business_id,
            json.dumps(payload),
            estimated_revenue,
            datetime.utcnow()
        )
    )

    inspection_id = cur.lastrowid

    conn.commit()
    conn.close()

    return inspection_id


# =========================================================
# LIST INSPECTION RUNS
# =========================================================

def list_inspection_runs(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, estimated_revenue, created_at
        FROM inspection_runs
        WHERE username = ?
        ORDER BY created_at DESC
        """,
        (username,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows


# =========================================================
# LOAD INSPECTION PAYLOAD
# =========================================================

def load_inspection_payload(inspection_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT payload
        FROM inspection_runs
        WHERE id = ?
        """,
        (inspection_id,)
    )

    row = cur.fetchone()

    conn.close()

    if not row:
        return None

    try:
        return json.loads(row[0])
    except Exception:
        return {}


# =========================================================
# INSPECTION ANALYTICS
# =========================================================

def get_inspection_analytics(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*), COALESCE(SUM(estimated_revenue),0)
        FROM inspection_runs
        WHERE username = ?
        """,
        (username,)
    )

    total_runs, total_revenue = cur.fetchone()

    conn.close()

    avg_score = 0

    if total_runs > 0:
        avg_score = round(total_revenue / total_runs)

    return {
        "total_runs": total_runs,
        "total_revenue": total_revenue,
        "average_score": avg_score
    }


# =========================================================
# CONVERSION METRICS
# =========================================================

def get_inspection_conversion_metrics(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM inspection_runs
        WHERE username = ?
        """,
        (username,)
    )

    total = cur.fetchone()[0]

    conn.close()

    return {
        "total_inspections": total,
        "conversion_rate": 0
    }


# =========================================================
# TIER DISTRIBUTION
# =========================================================

def get_inspection_tier_distribution(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT payload
        FROM inspection_runs
        WHERE username = ?
        """,
        (username,)
    )

    rows = cur.fetchall()

    tiers = {"low": 0, "medium": 0, "high": 0}

    for r in rows:

        try:
            payload = json.loads(r[0])
        except Exception:
            continue

        tier = payload.get("lead_tier")

        if tier in tiers:
            tiers[tier] += 1

    conn.close()

    return tiers


# =========================================================
# REVENUE TREND
# =========================================================

def get_inspection_revenue_trend(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT created_at, estimated_revenue
        FROM inspection_runs
        WHERE username = ?
        ORDER BY created_at
        """,
        (username,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows