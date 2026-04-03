# -*- coding: utf-8 -*-

# =========================================================
# 🔥 CRITICAL — DB INIT MUST RUN FIRST (NO IMPORT DEPENDENCIES)
# =========================================================

import os
import sys
import subprocess

from core.db import initialize_database, verify_schema_version

print("🚀 Booting SwarmDigiz...")

# Ensure schema version
verify_schema_version()

# Ensure tables exist BEFORE anything else touches DB
initialize_database()

print("✅ Database initialized successfully")


# =========================================================
# NORMAL IMPORTS (SAFE AFTER DB INIT)
# =========================================================

import streamlit as st

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from core.business_service import get_or_create_business
from core.subscription_guard import verify_subscription

# 🔥 IMPORT YOUR FLASK API
from api.inspection_api import inspection_bp
from flask import Flask

from ui.app_shell import (
    APP_NAME,
    init_session,
    resolve_embed_mode,
    require_login,
    resolve_username,
    sidebar,
)

from ui.growth_dashboard_page import render_growth_dashboard
from ui.marketing_page import render_marketing_swarm_page
from ui.inspector_page import render_visual_inspector_page
from ui.inspection_history_page import render_inspection_history
from ui.campaign_builder_page import render_campaign_builder
from ui.lead_pipeline_page import render_lead_pipeline
from ui.embed_generator_page import render_embed_generator
from ui.campaign_analytics_page import render_campaign_analytics
from ui.services_page import render_services_page
from ui.billing_page import render_billing_page
from ui.admin_dashboard_page import render_admin_dashboard


# =========================================================
# 🔥 FLASK API APP (EMBEDDED)
# =========================================================

flask_app = Flask(__name__)
flask_app.register_blueprint(inspection_bp)


# =========================================================
# DATABASE MIGRATIONS (RUN AFTER INIT — SAFE)
# =========================================================


def run_db_migrations():
    try:
        env = os.environ.copy()
        env["ALLOW_SCHEMA_MUTATION"] = "true"

        subprocess.run([sys.executable, "db/migrate.py"], check=True, env=env)

        print("✅ Database migrations applied")

    except Exception as e:
        print(f"⚠️ Migration runner skipped or failed: {e}")


run_db_migrations()


# =========================================================
# STREAMLIT BOOT
# =========================================================

st.set_page_config(page_title=APP_NAME, layout="wide")

embed_mode = resolve_embed_mode()
init_session()


# =========================================================
# 🔥 NEW — GLOBAL NAV STATE (BUTTON FIX)
# =========================================================

if "nav" not in st.session_state:
    st.session_state["nav"] = None


# ---------------------------------------------------------
# AUTH
# ---------------------------------------------------------

require_login(embed_mode)
username = resolve_username()


# ---------------------------------------------------------
# SUBSCRIPTION
# ---------------------------------------------------------

if not embed_mode:

    if not verify_subscription(username):
        st.warning("⚠️ Active subscription required to access SwarmDigiz")
        render_billing_page()
        st.stop()


# ---------------------------------------------------------
# BUSINESS CONTEXT
# ---------------------------------------------------------

if "business_name" not in st.session_state:
    st.session_state["business_name"] = "Swarm Business"

business_id = get_or_create_business(username, st.session_state["business_name"])

st.session_state["business_id"] = business_id


# =========================================================
# ROUTER
# =========================================================

if embed_mode:
    render_visual_inspector_page(username, business_id)
    st.stop()
else:
    app_mode = sidebar(APP_NAME, username)


# =========================================================
# 🔥 BUTTON NAV OVERRIDE (CRITICAL FIX)
# =========================================================

nav = st.session_state.get("nav")

if nav == "inspector":
    render_visual_inspector_page(username, business_id)
    st.stop()

elif nav == "booking":
    st.success("🚀 Booking flow coming next")
    st.stop()


# =========================================================
# PAGE ROUTING
# =========================================================

if app_mode == "AI Growth Dashboard":
    render_growth_dashboard(business_id)

elif app_mode == "Lead Pipeline":
    render_lead_pipeline(business_id)

elif app_mode == "Visual Inspector":
    render_visual_inspector_page(username, business_id)

elif app_mode == "Marketing Swarm":
    render_marketing_swarm_page(username, business_id)

elif app_mode == "Campaign Builder":
    render_campaign_builder(username, business_id)

elif app_mode == "Campaign Analytics":
    render_campaign_analytics(business_id)

elif app_mode == "Inspection History":
    render_inspection_history(business_id)

elif app_mode == "Embed Inspector":
    render_embed_generator(business_id)

elif app_mode == "Services":
    render_services_page(business_id)

elif app_mode == "Billing":
    render_billing_page()

elif app_mode == "Admin Dashboard":

    if username != "admin":
        st.error("⛔ Admin access only")
        st.stop()

    render_admin_dashboard()

else:
    render_visual_inspector_page(username, business_id)
