import os
import sqlite3
import threading
import time
import random

from flask import Flask, request, jsonify, Blueprint, make_response
from flask_cors import CORS
from twilio.rest import Client

# =========================================================
# APP INIT
# =========================================================

app = Flask(__name__)

# Keep Flask-CORS enabled
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

inspection_bp = Blueprint("inspection", __name__)

# =========================================================
# GLOBAL RESPONSE HEADERS (BULLETPROOF CORS)
# =========================================================

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, ngrok-skip-browser-warning"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


# =========================================================
# DB PATH
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "swarmdigiz.db")


# =========================================================
# TWILIO CONFIG
# =========================================================

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "").strip()
OWNER_ALERT_PHONE = os.getenv("OWNER_ALERT_PHONE", "").strip()

twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    print("✅ Twilio initialized")
else:
    print("⚠️ Twilio NOT configured")


# =========================================================
# IMAGE DETECTION
# =========================================================

def detect_condition_from_image(file):
    return random.choice(["clean", "moderate", "heavy"])


# =========================================================
# PRICING ENGINE
# =========================================================

def estimate_quote(service, size, condition):
    base_pricing = {
        "air_duct": 200,
        "dryer_vent": 100,
        "carpet": 150,
        "tile": 180
    }

    condition_multiplier = {
        "clean": 1.0,
        "moderate": 1.25,
        "heavy": 1.5
    }

    base = base_pricing.get(service, 150)
    size_factor = 1 + (size * 0.15)
    multiplier = condition_multiplier.get(condition, 1.0)

    return int(base * size_factor * multiplier)


# =========================================================
# LEAD SCORING
# =========================================================

def score_lead(size, condition):
    score = 50

    if size >= 3:
        score += 15
    if size >= 5:
        score += 15

    if condition == "moderate":
        score += 10
    elif condition == "heavy":
        score += 20

    if score >= 85:
        tier = "hot"
    elif score >= 65:
        tier = "warm"
    else:
        tier = "cold"

    return score, tier


# =========================================================
# HELPERS
# =========================================================

def prettify_service(service):
    labels = {
        "air_duct": "air duct cleaning",
        "dryer_vent": "dryer vent cleaning",
        "carpet": "carpet cleaning",
        "tile": "tile and grout cleaning"
    }
    return labels.get(service, service.replace("_", " "))


# =========================================================
# SMS
# =========================================================

def send_sms(to_number, message):
    if not to_number:
        return False

    if not twilio_client or not TWILIO_PHONE_NUMBER:
        print(f"⚠️ SMS skipped (no config) → {to_number}: {message}")
        return False

    try:
        twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        print(f"✅ SMS sent → {to_number}")
        return True
    except Exception as e:
        print(f"❌ SMS failed: {e}")
        return False


# =========================================================
# FOLLOW-UP ENGINE
# =========================================================

def schedule_followups(phone, customer_name, quote, service_label, lead_tier):
    """
    Simple background follow-up engine.
    For real flow:
    - hot: 1 hour, next day
    - warm: 5 minutes, next day
    - cold: next day only

    For quick testing, temporarily reduce sleep values.
    """

    if not phone:
        return

    def run():
        try:
            if lead_tier == "hot":
                time.sleep(3600)
                send_sms(
                    phone,
                    f"Hi {customer_name}, just checking in on your {service_label} estimate of ${quote}. "
                    f"We still have availability. Reply YES to move forward or book here: https://calendly.com/airductify/30mins"
                )

                time.sleep(86400)
                send_sms(
                    phone,
                    f"Final reminder for your {service_label} estimate of ${quote}. "
                    f"If you'd like to reserve a spot, reply YES or book now: https://calendly.com/airductify/30mins"
                )

            elif lead_tier == "warm":
                time.sleep(300)
                send_sms(
                    phone,
                    f"Hi {customer_name}, just following up on your {service_label} request. "
                    f"Your estimate is ${quote}. Reply YES if you'd like help booking with AirDuctify."
                )

                time.sleep(86400)
                send_sms(
                    phone,
                    f"We're still here if you'd like to move forward with your {service_label} service. "
                    f"Your estimate is ${quote}. Book now: https://calendly.com/airductify/30mins"
                )

            else:
                time.sleep(86400)
                send_sms(
                    phone,
                    f"Hi {customer_name}, if you still need help with {service_label}, "
                    f"AirDuctify can help. Book here: https://calendly.com/airductify/30mins"
                )

        except Exception as e:
            print(f"❌ Follow-up scheduler failed: {e}")

    threading.Thread(target=run, daemon=True).start()
    print(f"⏰ Follow-ups scheduled for {phone} ({lead_tier})")


# =========================================================
# FOLLOW-UP ORCHESTRATION
# =========================================================

def handle_sms_followup(phone, name, zip_code, lead_tier, quote, service):
    service_label = prettify_service(service)
    customer_name = name if name else "there"

    owner_message = (
        f"🚨 New {lead_tier.upper()} lead\n"
        f"Name: {customer_name}\n"
        f"Phone: {phone or 'N/A'}\n"
        f"ZIP: {zip_code or 'N/A'}\n"
        f"Service: {service_label}\n"
        f"Estimate: ${quote}"
    )

    if OWNER_ALERT_PHONE:
        send_sms(OWNER_ALERT_PHONE, owner_message)

    if not phone:
        return

    if lead_tier == "hot":
        send_sms(
            phone,
            f"Hi {customer_name}, thanks for contacting AirDuctify. "
            f"Your estimated {service_label} quote is ${quote}. "
            f"We have availability soon. Reply YES to move forward or book here: https://calendly.com/airductify/30mins"
        )

    elif lead_tier == "warm":
        print(f"🟡 Warm lead queued for delayed follow-up → {phone}")

    else:
        print(f"🔵 Cold lead saved, next-day nurture only → {phone}")

    schedule_followups(
        phone=phone,
        customer_name=customer_name,
        quote=quote,
        service_label=service_label,
        lead_tier=lead_tier
    )


# =========================================================
# UNIFIED INSPECTION ENDPOINT
# =========================================================

@inspection_bp.route("/api/inspection", methods=["POST", "OPTIONS"])
def create_inspection():

    if request.method == "OPTIONS":
        response = make_response(jsonify({"status": "ok"}), 200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, ngrok-skip-browser-warning"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response

    try:
        print("📥 Incoming inspection request")

        content_type = request.content_type or ""

        if content_type.startswith("multipart/form-data"):
            data = request.form.to_dict()
            file = request.files.get("file")
        else:
            data = request.get_json(silent=True) or {}
            file = None

        service = data.get("service_type")
        size = data.get("home_size")
        business = data.get("business_id")
        condition = data.get("condition")
        phone = (data.get("phone") or "").strip()
        name = (data.get("name") or "").strip()
        zip_code = (data.get("zip") or "").strip()

        if not service:
            return jsonify({"error": "Missing service_type"}), 400

        if size is None or size == "":
            return jsonify({"error": "Missing home_size"}), 400

        try:
            size = int(size)
        except (TypeError, ValueError):
            return jsonify({"error": "home_size must be integer"}), 400

        # -----------------------------------------
        # IMAGE → CONDITION
        # -----------------------------------------
        if file:
            condition = detect_condition_from_image(file)

        if not condition:
            condition = "clean"

        # -----------------------------------------
        # ENGINE
        # -----------------------------------------
        quote = estimate_quote(service, size, condition)
        lead_score, lead_tier = score_lead(size, condition)

        print(f"🧠 Engine → Quote: {quote}, Tier: {lead_tier}")

        # -----------------------------------------
        # SAVE
        # -----------------------------------------
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO inspection_runs(
            service_type,
            estimated_quote,
            lead_score,
            lead_tier,
            booking_status,
            business_id,
            username
        )
        VALUES(?,?,?,?,?,?,?)
        """, (
            service,
            quote,
            lead_score,
            lead_tier,
            "new",
            business,
            name or "guest"
        ))

        conn.commit()
        conn.close()

        print("💾 Saved to DB")

        # -----------------------------------------
        # SMS + FOLLOWUPS
        # -----------------------------------------
        handle_sms_followup(
            phone=phone,
            name=name,
            zip_code=zip_code,
            lead_tier=lead_tier,
            quote=quote,
            service=service
        )

        print("📲 SMS logic executed")

        return jsonify({
            "success": True,
            "quote": quote,
            "condition": condition,
            "lead_score": lead_score,
            "lead_tier": lead_tier
        })

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": str(e)}), 500


# =========================================================
# REGISTER + RUN
# =========================================================

app.register_blueprint(inspection_bp)

if __name__ == "__main__":
    print("🚀 Starting Inspection API...")
    app.run(host="0.0.0.0", port=5000, debug=True)