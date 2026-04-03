import streamlit as st
import sqlite3


DB_PATH = "swarmdigiz/swarmdigiz.db"


def get_existing_columns(cur):
    cur.execute("PRAGMA table_info(inspection_runs)")
    cols = cur.fetchall()
    return [c[1] for c in cols]


def load_leads(business_id: int):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    columns = get_existing_columns(cur)

    # Default safe fallbacks
    select_fields = ["id"]

    if "service_type" in columns:
        select_fields.append("service_type")
    else:
        select_fields.append("'unknown' as service_type")

    if "lead_score" in columns:
        select_fields.append("lead_score")
    else:
        select_fields.append("0 as lead_score")

    if "lead_tier" in columns:
        select_fields.append("lead_tier")
    else:
        select_fields.append("'cold' as lead_tier")

    if "estimated_quote" in columns:
        select_fields.append("estimated_quote")
    else:
        select_fields.append("0 as estimated_quote")

    if "booking_status" in columns:
        select_fields.append("booking_status")
    else:
        select_fields.append("'new' as booking_status")

    if "created_at" in columns:
        select_fields.append("created_at")
    else:
        select_fields.append("CURRENT_TIMESTAMP as created_at")

    query = f"""
        SELECT
            {",".join(select_fields)}
        FROM inspection_runs
        WHERE business_id = ?
        ORDER BY created_at DESC
    """

    cur.execute(query, (business_id,))
    rows = cur.fetchall()

    conn.close()

    return rows


def render_lead_pipeline(business_id: int):

    st.title("📊 Lead Pipeline")

    leads = load_leads(business_id)

    if not leads:
        st.info("No leads yet. Run the Visual Inspector to generate leads.")
        return

    st.markdown("### Active Leads")

    for lead in leads:

        (
            lead_id,
            service,
            score,
            tier,
            quote,
            status,
            created
        ) = lead

        with st.container():

            c1, c2, c3, c4, c5, c6 = st.columns(6)

            c1.write(f"**#{lead_id}**")
            c2.write(service or "unknown")
            c3.metric("Score", score if score else 0)
            c4.write(tier or "unknown")
            c5.write(f"${quote}" if quote else "$0")
            c6.write(status or "new")

            action_col1, action_col2, action_col3 = st.columns(3)

            if action_col1.button("📢 Campaign", key=f"campaign_{lead_id}"):
                st.session_state["selected_lead"] = lead_id
                st.success("Open Campaign Builder to generate ads.")

            if action_col2.button("📅 Book", key=f"book_{lead_id}"):
                st.success("Booking flow will open here.")

            if action_col3.button("☎ Contacted", key=f"contact_{lead_id}"):
                update_status(lead_id, "contacted")
                st.rerun()

            st.markdown("---")


def update_status(lead_id, status):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        UPDATE inspection_runs
        SET booking_status = ?
        WHERE id = ?
    """, (status, lead_id))

    conn.commit()
    conn.close()