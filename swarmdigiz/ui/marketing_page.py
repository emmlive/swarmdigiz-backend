import streamlit as st

from main import run_marketing_swarm, AGENT_REGISTRY, GOAL_TO_AGENTS
from exporters.structured_output import build_structured_output

from connectors.facebook_ads_connector import FacebookAdsConnector
from connectors.google_ads_connector import GoogleAdsConnector

from core.swarm_service import (
    create_swarm_run,
    save_swarm_output,
    list_swarm_runs,
    load_swarm_outputs,
    get_run_metadata,
)

from core.connector_service import log_connector_execution


def _render_outputs(outputs: dict):
    st.markdown("### 📦 Swarm Outputs")

    for agent, text in outputs.items():
        with st.expander(f"{agent}", expanded=False):
            st.write(text)


def render_marketing_swarm_page(username: str, business_id: int):

    # =================================================
    # 🔥 HERO SECTION (NEW — BUTTON FIX)
    # =================================================

    st.markdown(
        """
    <h1 style="font-size:42px; margin-bottom:10px;">
    Fast, Reliable Cleaning Services
    </h1>
    <p style="color:#94a3b8; font-size:18px;">
    Air duct, dryer vent, carpet & tile cleaning — simple pricing, fast scheduling, no surprises.
    </p>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Get Your Estimate", use_container_width=True):
            st.session_state["nav"] = "inspector"

    with col2:
        if st.button("Book Service Now", use_container_width=True):
            st.session_state["nav"] = "booking"

    st.markdown("---")

    # =================================================
    # ORIGINAL PAGE CONTENT (UNCHANGED)
    # =================================================

    st.title("⚡ Grow My Business")

    # =================================================
    # Run History
    # =================================================

    st.markdown("### 🕒 Run History")

    runs = list_swarm_runs(username) or []

    selected_run_id = None

    if runs:

        options = [f"Run #{r[0]} • {r[1]} • {r[2]}" for r in runs]

        selected = st.selectbox("Select Run (optional)", ["—"] + options)

        if selected != "—":

            selected_run_id = int(selected.split("#")[1].split(" ")[0])

            meta = get_run_metadata(selected_run_id) or {}

            st.session_state["business_name"] = meta.get(
                "business_name"
            ) or st.session_state.get("business_name")

            st.session_state["mode"] = meta.get("mode") or st.session_state.get("mode")

            st.session_state["selected_goal"] = meta.get("goal")
            st.session_state["selected_agents"] = meta.get("active_swarm") or []

            st.session_state["selected_run_id"] = selected_run_id

            existing = load_swarm_outputs(selected_run_id) or {}

            if existing:
                _render_outputs(existing)

    st.markdown("---")

    # =================================================
    # Swarm Runner
    # =================================================

    st.text_input("Business Name", key="business_name")

    st.radio("Mode", ["Simple", "Advanced"], key="mode")

    if st.session_state["mode"] == "Simple":

        st.selectbox("Goal", list(GOAL_TO_AGENTS.keys()), key="selected_goal")

    else:

        st.multiselect("Agents", list(AGENT_REGISTRY.keys()), key="selected_agents")

    if st.button("🚀 Run Swarm"):

        metadata = {
            "business_name": st.session_state["business_name"],
            "mode": st.session_state["mode"],
            "goal": (
                st.session_state["selected_goal"]
                if st.session_state["mode"] == "Simple"
                else None
            ),
            "active_swarm": (
                st.session_state["selected_agents"]
                if st.session_state["mode"] == "Advanced"
                else None
            ),
        }

        run_id = create_swarm_run(username, metadata, business_id)

        payload = {"business_name": metadata["business_name"]}

        if metadata["mode"] == "Simple":
            payload["goal"] = metadata["goal"]
        else:
            payload["active_swarm"] = metadata["active_swarm"]

        results = run_marketing_swarm(payload)

        for agent_name, output_text in results.items():
            save_swarm_output(run_id, agent_name, output_text)

        st.session_state["selected_run_id"] = run_id
        st.session_state["__last_swarm_results__"] = results

        st.success(f"Saved Run #{run_id}")

        _render_outputs(results)

    # =================================================
    # One-Click Campaign Launch
    # =================================================

    results = st.session_state.get("__last_swarm_results__")

    st.markdown("---")
    st.markdown("### 🚀 One-Click Campaign Launch")

    if not results and st.session_state.get("selected_run_id"):

        results = load_swarm_outputs(st.session_state["selected_run_id"]) or None

    if results:

        if st.button("Launch Ads Campaigns (Google + Facebook)"):

            raw_agents = [
                {"agent": name, "output": text} for name, text in results.items()
            ]

            structured = build_structured_output(results, raw_agents)

            fb = FacebookAdsConnector().execute(structured)
            google = GoogleAdsConnector().execute(structured)

            log_connector_execution(username, "facebook_ads", fb)
            log_connector_execution(username, "google_ads", google)

            st.success("Campaigns launched")

            st.json({"facebook": fb, "google": google})

    else:

        st.info(
            "Run a swarm (or select a past run) to enable one-click campaign launch."
        )
