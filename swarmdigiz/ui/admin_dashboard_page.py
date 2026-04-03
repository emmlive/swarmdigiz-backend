# -*- coding: utf-8 -*-

import streamlit as st
import sqlite3

from core.admin_service import list_users, update_subscription
from core.ai_operations_monitor import check_system_health

DB_PATH = "swarmdigiz/swarmdigiz.db"


def get_admin_metrics():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute("SELECT COUNT(*) FROM users")
        users = cur.fetchone()[0]
    except:
        users = 0

    try:
        cur.execute("SELECT COUNT(*) FROM businesses")
        businesses = cur.fetchone()[0]
    except:
        businesses = 0

    try:
        cur.execute("SELECT COUNT(*) FROM inspection_runs")
        inspections = cur.fetchone()[0]
    except:
        inspections = 0

    try:
        cur.execute("SELECT SUM(estimated_revenue) FROM inspection_runs")
        revenue = cur.fetchone()[0] or 0
    except:
        revenue = 0

    conn.close()

    return users, businesses, inspections, revenue


def render_admin_dashboard():

    st.title("🛠 SwarmDigiz Super Admin")

    users, businesses, inspections, revenue = get_admin_metrics()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Users", users)
    c2.metric("Businesses", businesses)
    c3.metric("Inspections", inspections)
    c4.metric("Revenue", f"${revenue}")

    st.markdown("---")

    # =====================================================
    # AI Operations Monitor
    # =====================================================

    st.subheader("🤖 AI Operations Monitor")

    issues = check_system_health()

    for i in issues:
        st.write(i)

    st.markdown("---")

    # =====================================================
    # USER MANAGEMENT
    # =====================================================

    st.subheader("👥 User Subscription Management")

    users = list_users()

    if users:

        for username, status in users:

            col1, col2, col3 = st.columns([2,2,2])

            col1.write(username)
            col2.write(f"Current: {status}")

            new_status = col3.selectbox(
                "Change Plan",
                ["free", "active"],
                key=username
            )

            if st.button("Update", key=f"btn_{username}"):

                update_subscription(username, new_status)

                st.success(f"{username} updated to {new_status}")

    else:

        st.info("No users found")