# =========================================================
# SWARMDIGIZ STRIPE WEBHOOK LISTENER
# =========================================================

import os
import sys
import stripe

from flask import Flask, request, jsonify

# =========================================================
# PROJECT PATH FIX
# Allows running script from project root
# =========================================================

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

# =========================================================
# INTERNAL IMPORTS
# =========================================================

from swarmdigiz.core.stripe_service import update_subscription
from swarmdigiz.core.payment_status_service import handle_successful_payment


# =========================================================
# STRIPE CONFIG
# =========================================================

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

if not stripe.api_key:
    print("⚠️ STRIPE_SECRET_KEY not set")

if not endpoint_secret:
    print("⚠️ STRIPE_WEBHOOK_SECRET not set")


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# STRIPE WEBHOOK ROUTE
# =========================================================

@app.route("/stripe-webhook", methods=["POST"])
def stripe_webhook():

    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    # -----------------------------------------------------
    # VERIFY EVENT
    # -----------------------------------------------------

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            endpoint_secret
        )

    except stripe.error.SignatureVerificationError:
        print("❌ Invalid Stripe signature")
        return jsonify({"error": "Invalid signature"}), 400

    except Exception as e:
        print("❌ Webhook error:", e)
        return jsonify({"error": str(e)}), 400

    event_type = event["type"]

    print(f"🔔 Stripe Event Received: {event_type}")

    # =====================================================
    # CHECKOUT COMPLETED (PAYMENT + SUBSCRIPTION)
    # =====================================================

    if event_type == "checkout.session.completed":

        session = event["data"]["object"]

        customer_id = session.get("customer")
        metadata = session.get("metadata", {})
        session_id = session.get("id")

        # ---------------------------------------------
        # 1. HANDLE PAYMENT FLOW (NEW)
        # ---------------------------------------------

        if metadata:
            try:
                handle_successful_payment(session_id, metadata)
                print(f"✅ Payment lifecycle completed for session {session_id}")
            except Exception as e:
                print("❌ Payment handling error:", e)

        # ---------------------------------------------
        # 2. HANDLE SUBSCRIPTION (EXISTING)
        # ---------------------------------------------

        if customer_id:
            try:
                update_subscription(
                    customer_id,
                    "active",
                    "paid"
                )
                print(f"✅ Subscription activated for {customer_id}")
            except Exception as e:
                print("❌ Subscription update error:", e)

    # =====================================================
    # SUBSCRIPTION CANCELLED
    # =====================================================

    elif event_type == "customer.subscription.deleted":

        subscription = event["data"]["object"]

        customer_id = subscription.get("customer")

        if customer_id:
            try:
                update_subscription(
                    customer_id,
                    "cancelled",
                    "free"
                )
                print(f"⚠️ Subscription cancelled for {customer_id}")
            except Exception as e:
                print("❌ Subscription cancel error:", e)

    # =====================================================
    # OPTIONAL: PAYMENT FAILED / EXPIRED
    # =====================================================

    elif event_type == "checkout.session.expired":
        session = event["data"]["object"]
        print(f"⚠️ Checkout expired: {session.get('id')}")

    # =====================================================
    # RETURN SUCCESS
    # =====================================================

    return jsonify({"status": "success"}), 200


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    print("🚀 Stripe Webhook Listener running on port 5000")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )