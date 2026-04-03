# -*- coding: utf-8 -*-

import hashlib
import json
import sqlite3
from datetime import datetime, timedelta

import streamlit as st
import streamlit.components.v1 as components

from core.payment_service import build_payment_options, create_checkout_session

# ✅ NEW IMPORTS
from core.calendar_service import generate_time_slots, is_valid_date, format_appointment

DB_PATH = "swarmdigiz/swarmdigiz.db"


# =========================================================
# DB HELPERS
# =========================================================


def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def save_booking(data: dict) -> bool:
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_id TEXT,
                customer_name TEXT,
                customer_email TEXT,
                customer_phone TEXT,
                package_name TEXT,
                payment_type TEXT,
                quoted_total INTEGER,
                selected_total INTEGER,
                appointment_date TEXT,
                appointment_time TEXT,
                status TEXT,
                raw_data TEXT,
                created_at TEXT
            )
        """
        )

        cur.execute(
            """
            INSERT INTO bookings (
                business_id,
                customer_name,
                customer_email,
                customer_phone,
                package_name,
                payment_type,
                quoted_total,
                selected_total,
                appointment_date,
                appointment_time,
                status,
                raw_data,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                str(data.get("business_id", "")),
                data.get("customer_name", ""),
                data.get("customer_email", ""),
                data.get("customer_phone", ""),
                data.get("package_name", ""),
                data.get("payment_type", ""),
                int(data.get("quoted_total", 0)),
                int(data.get("selected_total", 0)),
                data.get("appointment_date", ""),
                data.get("appointment_time", ""),
                data.get("status", "initiated"),
                json.dumps(data),
                datetime.utcnow().isoformat(),
            ),
        )

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print("❌ save_booking failed:", e)
        return False


# =========================================================
# GLOBAL STATE INIT
# =========================================================


def init_global_state():
    defaults = {
        "quote": None,
        "selected_tier": None,
        "selected_payment": "full",
        "selected_payment_radio": "full",
        "checkout_session_id": None,
        "checkout_url": None,
        "booking": None,
        "quote_signature": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =========================================================
# HELPERS
# =========================================================


def build_tiers(base_price: int):
    return {
        "Basic": {
            "price": int(round(base_price * 0.85)),
            "features": [
                "Standard cleaning",
                "Basic inspection",
                "No warranty",
            ],
            "label": "Good",
        },
        "Recommended": {
            "price": int(round(base_price)),
            "features": [
                "Deep cleaning",
                "Full system inspection",
                "30-day warranty",
            ],
            "label": "Best Value ⭐",
        },
        "Premium": {
            "price": int(round(base_price * 1.25)),
            "features": [
                "Deep cleaning + sanitization",
                "Priority scheduling",
                "90-day warranty",
            ],
            "label": "Premium",
        },
    }


def urgency_banner():
    deadline = datetime.now() + timedelta(hours=2)
    st.warning(
        f"⚠️ Limited availability today — secure your spot before "
        f"{deadline.strftime('%I:%M %p')}"
    )


def resolve_base_price(quote: dict) -> int:
    candidate_keys = [
        "total",
        "total_price",
        "estimated_total",
        "estimated_price",
        "price",
        "quote_total",
        "amount",
        "subtotal",
        "quote_price",
    ]

    for key in candidate_keys:
        value = quote.get(key)
        if value is None:
            continue

        try:
            numeric = float(value)
            if numeric > 0:
                return int(round(numeric))
        except Exception:
            continue

    return 0


def build_quote_signature(quote: dict) -> str:
    try:
        normalized = str(sorted(quote.items())).encode("utf-8")
    except Exception:
        normalized = str(quote).encode("utf-8")

    return hashlib.md5(normalized).hexdigest()


def initialize_quote_state(signature: str):
    if st.session_state.get("quote_signature") != signature:
        st.session_state["quote_signature"] = signature
        st.session_state["selected_tier"] = None
        st.session_state["selected_payment"] = "full"
        st.session_state["selected_payment_radio"] = "full"
        st.session_state["checkout_session_id"] = None
        st.session_state["checkout_url"] = None
        st.session_state["booking"] = None


def resolve_customer_details() -> dict:
    return {
        "customer_name": st.session_state.get("customer_name", ""),
        "customer_email": st.session_state.get("customer_email", ""),
        "customer_phone": st.session_state.get("customer_phone", ""),
        "business_id": st.session_state.get("business_id", ""),
    }


# =========================================================
# MAIN PANEL
# =========================================================


def render_visual_quote_panel(quote):

    init_global_state()

    if not quote:
        st.error("No quote available")
        return

    signature = build_quote_signature(quote)
    initialize_quote_state(signature)

    base_price = resolve_base_price(quote)

    st.markdown("## 💰 Your Instant Quote")
    urgency_banner()
    st.markdown("---")

    if base_price <= 0:
        st.error("Quote total is $0. Cannot proceed.")
        with st.expander("View Quote Payload"):
            st.json(quote)
        return

    tiers = build_tiers(base_price)
    cols = st.columns(3)

    for i, (name, data) in enumerate(tiers.items()):
        with cols[i]:
            st.markdown(f"### {data['label']}")
            st.markdown(f"## ${data['price']}")

            for feature in data["features"]:
                st.write(f"✔ {feature}")

            if name == "Recommended":
                st.success("Most Popular")

            if st.button(f"Select {name}", key=f"tier_{name}"):
                st.session_state["selected_tier"] = name
                st.session_state["selected_payment"] = "full"
                st.session_state["selected_payment_radio"] = "full"
                st.session_state["checkout_session_id"] = None
                st.session_state["checkout_url"] = None
                st.session_state["booking"] = None
                st.rerun()

    st.markdown("---")

    selected_tier = st.session_state.get("selected_tier")

    if not selected_tier:
        st.info("Select a package to continue")
        return

    tier = tiers[selected_tier]

    st.success(f"{selected_tier} Package Selected")
    st.markdown(f"## Total: ${tier['price']}")

    # PAYMENT
    st.markdown("### 💳 Payment Options")

    payment_options = build_payment_options(tier["price"])

    selected_payment = st.radio(
        "Choose payment:",
        options=list(payment_options.keys()),
        format_func=lambda k: f"{payment_options[k]['label']} (${payment_options[k]['amount']})",
        key="selected_payment_radio",
    )

    st.session_state["selected_payment"] = selected_payment
    payment = payment_options[selected_payment]

    st.success(f"{payment['label']} — ${payment['amount']}")

    # -----------------------------------------------------
    # CALENDAR (NEW - MODULAR)
    # -----------------------------------------------------

    st.markdown("### 📅 Select Appointment")

    selected_date = st.date_input("Choose a date", min_value=datetime.today())

    selected_time = st.selectbox("Choose a time", generate_time_slots())

    st.session_state["appointment_date"] = str(selected_date)
    st.session_state["appointment_time"] = selected_time

    # BOOKING
    customer = resolve_customer_details()

    booking_payload = {
        "business_id": customer.get("business_id", ""),
        "customer_name": customer.get("customer_name", ""),
        "customer_email": customer.get("customer_email", ""),
        "customer_phone": customer.get("customer_phone", ""),
        "package_name": selected_tier,
        "payment_type": selected_payment,
        "quoted_total": tier["price"],
        "selected_total": payment["amount"],
        "appointment_date": st.session_state.get("appointment_date"),
        "appointment_time": st.session_state.get("appointment_time"),
        "status": "initiated",
        "quote": quote,
        "timestamp": datetime.utcnow().isoformat(),
    }

    # CHECKOUT
    if st.button("🚀 Secure Your Spot", key="secure_your_spot_btn"):

        if not is_valid_date(selected_date):
            st.error("Please select a valid date")
            return

        if not selected_time:
            st.error("Please select a time")
            return

        st.session_state["booking"] = booking_payload.copy()
        save_booking(st.session_state["booking"])

        session = create_checkout_session(
            int(payment["amount"] * 100),
            metadata={
                "business_id": str(customer.get("business_id")),
                "tier": selected_tier,
                "payment_type": selected_payment,
                "appointment": format_appointment(selected_date, selected_time),
            },
        )

        if not session.get("success"):
            st.error(session.get("error", "Checkout failed"))
        else:
            url = session["checkout_url"]

            st.success("Redirecting to secure checkout...")
            st.markdown(f"[Click here if not redirected]({url})")

            components.html(
                f"""<script>window.top.location.href="{url}"</script>""",
                height=0,
            )

    st.markdown("---")
