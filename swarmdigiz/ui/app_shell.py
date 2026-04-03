# ui/app_shell.py
import streamlit as st

from core.auth_engine import verify_user

APP_NAME = "SwarmDigiz"

DEFAULTS = {
    "authenticated": None,
    "username": None,
    "selected_run_id": None,
    "selected_inspection_id": None,
    "business_name": "My Business",
    "business_id": None,
    "mode": "Simple",
    "selected_goal": None,
    "selected_agents": [],
}


# ---------------------------------------------------------
# SESSION INIT
# ---------------------------------------------------------

def init_session():
    # Single source of truth
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ---------------------------------------------------------
# EMBED MODE
# ---------------------------------------------------------

def resolve_embed_mode():
    qp = st.query_params
    return qp.get("embed") == "true"


# ---------------------------------------------------------
# LOGIN SYSTEM
# ---------------------------------------------------------

def require_login(embed_mode: bool):

    # Embedded inspectors bypass login
    if embed_mode:
        return

    if not st.session_state.get("authenticated"):

        st.title("🔐 SwarmDigiz Login")

        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")

        if st.button("Login"):

            if not username_input or not password_input:
                st.error("Username and password required")
                st.stop()

            business_id = verify_user(username_input, password_input)

            if business_id:

                st.session_state["authenticated"] = True
                st.session_state["username"] = username_input
                st.session_state["business_id"] = business_id

                st.rerun()

            else:

                st.error("Invalid username or password")

        st.stop()


# ---------------------------------------------------------
# USERNAME RESOLUTION
# ---------------------------------------------------------

def resolve_username():
    return st.session_state.get("username") or "embed_user"


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

def sidebar(app_name: str, username: str):

    with st.sidebar:

        st.markdown(f"## 🐝 {app_name}")
        st.caption(f"Signed in as `{username}`")

        # Full platform navigation
        app_mode = st.radio(
            "Choose Module",
            [
                "AI Growth Dashboard",
                "Lead Pipeline",
                "Visual Inspector",
                "Marketing Swarm",
                "Campaign Builder",
                "Campaign Analytics",
                "Inspection History",
                "Embed Inspector",
                "Services",
                "Billing",
                "Admin Dashboard",

            ],
        )

        st.markdown("---")

        logout = st.button("🚪 Logout")

        if logout:

            for k in list(st.session_state.keys()):
                st.session_state[k] = None

            st.rerun()

        return app_mode