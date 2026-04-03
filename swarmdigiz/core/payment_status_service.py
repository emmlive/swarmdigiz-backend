import sqlite3
from core.db import get_connection


# =========================================================
# MARK PAYMENT AS PAID
# =========================================================

def mark_job_paid(session_id: str, metadata: dict):
    """
    Called after Stripe webhook confirmation
    """

    try:
        conn = get_connection()
        cur = conn.cursor()

        # -------------------------------------
        # Extract metadata
        # -------------------------------------
        business_id = metadata.get("business_id")
        tier = metadata.get("tier")
        payment_type = metadata.get("payment_type")

        # -------------------------------------
        # Insert payment record
        # -------------------------------------
        cur.execute("""
            INSERT INTO payments (
                stripe_session_id,
                business_id,
                tier,
                payment_type,
                status
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            session_id,
            business_id,
            tier,
            payment_type,
            "paid"
        ))

        # -------------------------------------
        # Lock booking (example flag)
        # -------------------------------------
        cur.execute("""
            UPDATE inspection_runs
            SET status = 'booked'
            WHERE business_id = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (business_id,))

        conn.commit()
        conn.close()

        return True

    except Exception as e:
        print("❌ mark_job_paid error:", e)
        return False


# =========================================================
# STOP MARKETING (LEAD CONVERSION)
# =========================================================

def stop_marketing_for_lead(business_id: str):
    """
    Prevents further ad spend on converted lead
    """

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE leads
            SET status = 'converted'
            WHERE business_id = ?
            AND status != 'converted'
        """, (business_id,))

        conn.commit()
        conn.close()

        return True

    except Exception as e:
        print("❌ stop_marketing error:", e)
        return False


# =========================================================
# TRIGGER RETENTION FLOW
# =========================================================

def trigger_retention_flow(business_id: str):
    """
    Placeholder for:
    - SMS follow-up
    - Email nurture
    - Upsells
    """

    try:
        print(f"📩 Retention flow triggered for business {business_id}")
        return True

    except Exception as e:
        print("❌ retention error:", e)
        return False


# =========================================================
# MASTER HANDLER
# =========================================================

def handle_successful_payment(session_id: str, metadata: dict):
    """
    Central orchestration after payment success
    """

    try:
        business_id = metadata.get("business_id")

        mark_job_paid(session_id, metadata)
        stop_marketing_for_lead(business_id)
        trigger_retention_flow(business_id)

        print("✅ Payment lifecycle completed")

        return True

    except Exception as e:
        print("❌ payment handler error:", e)
        return False