import streamlit as st
from core.db import get_connection


def load_inspections(business_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            created_at,
            service_type,
            lead_score,
            lead_tier,
            estimated_quote,
            booking_status
        FROM inspection_runs
        WHERE business_id = ?
        ORDER BY created_at DESC
    """, (business_id,))

    rows = cur.fetchall()

    conn.close()

    return rows


def render_inspection_history(business_id):

    st.title("Inspection History")

    inspections = load_inspections(business_id)

    if not inspections:
        st.info("No inspections yet.")
        return

    for row in inspections:

        (
            inspection_id,
            created_at,
            service_type,
            lead_score,
            lead_tier,
            quote,
            status
        ) = row

        with st.container():

            col1, col2, col3, col4, col5 = st.columns(5)

            col1.write(f"#{inspection_id}")
            col2.write(service_type)
            col3.write(lead_tier)
            col4.write(f"${quote}")
            col5.write(status)

            st.divider()