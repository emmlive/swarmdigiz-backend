# -*- coding: utf-8 -*-

import json
import sqlite3

import streamlit as st

from modules.visual_inspector.payload_builder import build_inspection_payload
from modules.visual_inspector.visual_quote_panel import render_visual_quote_panel

from ai.visual_detection import analyze_image_condition
from ai.vent_counter import detect_vent_count

from core.retargeting_engine import generate_retargeting_signals
from core.lead_scoring_engine import calculate_lead_score
from core.quote_engine import generate_visual_quote
from core.inspection_service import create_inspection_run, get_inspection_analytics


DB_PATH = "swarmdigiz/swarmdigiz.db"


# =========================================================
# DB UTIL
# =========================================================


def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# LOAD SERVICES (HARDENED 🔥)
# =========================================================


def load_services(business_id):
    conn = get_connection()
    cur = conn.cursor()

    # 🔥 GUARANTEE TABLE EXISTS (CRITICAL FIX)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER,
            name TEXT,
            base_price REAL,
            config TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # 🔥 SEED DEFAULT SERVICES IF EMPTY
    cur.execute("SELECT COUNT(*) FROM services WHERE business_id = ?", (business_id,))
    count = cur.fetchone()[0]

    if count == 0:
        cur.executemany(
            """
            INSERT INTO services (business_id, name, base_price, config)
            VALUES (?, ?, ?, ?)
        """,
            [
                (business_id, "Air Duct Cleaning", 299, json.dumps({"vents": True})),
                (business_id, "Dryer Vent Cleaning", 149, json.dumps({})),
                (business_id, "Carpet Cleaning", 199, json.dumps({"rooms": True})),
            ],
        )
        conn.commit()

    # 🔥 SAFE QUERY
    cur.execute(
        """
        SELECT id, name, config
        FROM services
        WHERE business_id = ?
        """,
        (business_id,),
    )

    rows = cur.fetchall()
    conn.close()

    services = []

    for row in rows:
        config = {}

        if row["config"]:
            try:
                config = json.loads(row["config"])
            except Exception:
                config = {}

        services.append(
            {
                "id": row["id"],
                "name": row["name"],
                "config": config,
            }
        )

    return services


# =========================================================
# PAGE
# =========================================================


def render_visual_inspector_page(username: str, business_id: int):

    # -----------------------------------------------------
    # STEP STATE
    # -----------------------------------------------------

    if "vi_step" not in st.session_state:
        st.session_state["vi_step"] = "form"

    if "quote" not in st.session_state:
        st.session_state["quote"] = None

    st.title("🔍 Visual Inspector Engine")

    # -----------------------------------------------------
    # ANALYTICS
    # -----------------------------------------------------

    try:
        analytics = get_inspection_analytics(username)
    except Exception:
        analytics = {}

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Inspections", analytics.get("total_runs", 0))
    c2.metric("Estimated Revenue", f"${analytics.get('total_revenue', 0)}")
    c3.metric("Average Job Score", analytics.get("average_score", 0))

    st.markdown("---")

    step = st.session_state.get("vi_step", "form")

    # =====================================================
    # STEP 1 — FORM
    # =====================================================

    if step == "form":

        # -------------------------------------------------
        # PHOTO UPLOAD + AI
        # -------------------------------------------------

        st.markdown("### 📷 Upload Photo")

        uploaded_file = st.file_uploader(
            "Upload inspection image", type=["jpg", "jpeg", "png"]
        )

        ai_result = {}
        vent_result = {}

        if uploaded_file:
            try:
                ai_result = analyze_image_condition(uploaded_file) or {}
            except Exception:
                ai_result = {}

            try:
                vent_result = detect_vent_count(uploaded_file) or {}
            except Exception:
                vent_result = {}

            st.success("AI Analysis Complete")

            a, b, c = st.columns(3)
            a.metric("Condition", ai_result.get("condition", "unknown"))
            b.metric("Severity Score", ai_result.get("severity_score", 0))
            c.metric("Detected Vents", vent_result.get("vent_count", 0))

        st.markdown("---")

        # -------------------------------------------------
        # CUSTOMER INFO
        # -------------------------------------------------

        st.markdown("### 👤 Customer Information")

        customer_name = st.text_input("Customer Name")
        customer_email = st.text_input("Customer Email")
        customer_phone = st.text_input("Customer Phone")

        st.markdown("---")

        # -------------------------------------------------
        # SERVICES
        # -------------------------------------------------

        st.markdown("### 🧰 Select Services")

        services = load_services(business_id)

        if not services:
            st.warning("No services configured. Add services in the Services section.")
            return

        inspection_input = {"services": {}}

        for service in services:
            checked = st.checkbox(service["name"], key=f"service_{service['id']}")

            if checked:
                service_key = service["name"].lower().replace(" ", "_")
                service_data = {}

                for field, enabled in service["config"].items():
                    if not enabled:
                        continue

                    value = st.number_input(
                        field.replace("_", " ").title(),
                        min_value=0,
                        step=1,
                        key=f"{service['id']}_{field}",
                    )

                    service_data[field] = int(value)

                inspection_input["services"][service_key] = service_data

        st.markdown("---")

        # -------------------------------------------------
        # RUN INSPECTION
        # -------------------------------------------------

        if st.button("🔎 Run Inspection", key="run_inspection_btn"):

            if not customer_name:
                st.error("Customer name is required.")
                return

            if not inspection_input["services"]:
                st.error("Please select at least one service.")
                return

            try:
                payload = build_inspection_payload(inspection_input)
            except Exception as e:
                st.error(f"Payload build failed: {e}")
                return

            payload["customer"] = {
                "name": customer_name,
                "email": customer_email or "",
                "phone": customer_phone or "",
            }

            if ai_result:
                payload["ai_condition"] = ai_result.get("condition")
                payload["ai_severity"] = ai_result.get("severity_score")

            if vent_result:
                payload["detected_vents"] = vent_result.get("vent_count")

            try:
                payload.update(generate_retargeting_signals(payload))
            except Exception:
                pass

            try:
                payload.update(calculate_lead_score(payload))
            except Exception:
                pass

            try:
                create_inspection_run(username, payload, business_id)
            except Exception as e:
                st.error(f"Failed to save inspection: {e}")
                return

            try:
                quote = generate_visual_quote(payload)
            except Exception as e:
                st.error(f"Quote generation failed: {e}")
                return

            st.session_state["quote"] = quote
            st.session_state["vi_step"] = "quote"
            st.rerun()

    # =====================================================
    # STEP 2 — QUOTE
    # =====================================================

    elif step == "quote":

        quote = st.session_state.get("quote")

        if not quote:
            st.session_state["vi_step"] = "form"
            st.rerun()
            return

        render_visual_quote_panel(quote)

        st.markdown("---")

        if st.button("⬅️ Back to Form", key="back_to_form_btn"):
            st.session_state["vi_step"] = "form"
            st.session_state["quote"] = None
            st.rerun()
