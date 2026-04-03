# -*- coding: utf-8 -*-

import streamlit as st
import sqlite3
import json


DB_PATH = "swarmdigiz/swarmdigiz.db"


# =========================================================
# DATABASE
# =========================================================

def get_connection():
    return sqlite3.connect(DB_PATH)


def load_services(business_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, name, config
        FROM services
        WHERE business_id = ?
        ORDER BY id DESC
        """,
        (business_id,),
    )

    rows = cur.fetchall()
    conn.close()

    services = []

    for r in rows:
        config = {}

        if r[2]:
            try:
                config = json.loads(r[2])
            except:
                config = {}

        services.append(
            {
                "id": r[0],
                "name": r[1],
                "config": config,
            }
        )

    return services


def create_service(business_id, name, config):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO services (business_id, name, config)
        VALUES (?, ?, ?)
        """,
        (
            business_id,
            name,
            json.dumps(config),
        ),
    )

    conn.commit()
    conn.close()


def delete_service(service_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM services
        WHERE id = ?
        """,
        (service_id,),
    )

    conn.commit()
    conn.close()


# =========================================================
# UI
# =========================================================

def render_services_page(business_id):

    st.title("⚙ Service Configuration")

    st.markdown(
        """
Configure the services your business offers.

These services power the **Visual Inspector**, **Lead Intelligence**, and **Quote Engine**.
"""
    )

    st.markdown("---")

    services = load_services(business_id)

    if services:

        st.subheader("Configured Services")

        for s in services:

            col1, col2 = st.columns([6, 1])

            with col1:
                st.markdown(f"**{s['name']}**")

                if s["config"]:
                    st.caption(f"Config: {s['config']}")

            with col2:
                if st.button("Delete", key=f"delete_{s['id']}"):
                    delete_service(s["id"])
                    st.rerun()

    else:
        st.info("No services configured yet.")

    st.markdown("---")
    st.subheader("➕ Add New Service")

    service_name = st.text_input("Service Name")

    st.caption(
        "Optional configuration (JSON format). Example: {\"vent_count\": true}"
    )

    config_input = st.text_area("Configuration JSON", value="{}")

    if st.button("Add Service"):

        if not service_name.strip():
            st.error("Service name required.")
            return

        try:
            config = json.loads(config_input or "{}")
        except:
            st.error("Invalid JSON configuration.")
            return

        create_service(
            business_id,
            service_name.strip(),
            config,
        )

        st.success("Service added.")
        st.rerun()