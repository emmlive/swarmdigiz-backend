from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# =========================================
# ✅ TWILIO (RUNTIME SAFE — FIXED)
# =========================================
TWILIO_ENABLED = all(
    [
        os.environ.get("TWILIO_ACCOUNT_SID"),
        os.environ.get("TWILIO_AUTH_TOKEN"),
        os.environ.get("TWILIO_NUMBER"),
        os.environ.get("YOUR_PHONE_NUMBER"),
    ]
)

if TWILIO_ENABLED:
    from twilio.rest import Client


app = Flask(__name__)

# =========================================
# ✅ CORS (PRODUCTION SAFE)
# =========================================
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


# =========================================
# HEALTH CHECK
# =========================================
@app.route("/")
def home():
    return "API is running"


# =========================================
# INSPECTION ENDPOINT
# =========================================
@app.route("/api/inspection", methods=["POST"])
def inspection():
    try:
        print("\n=========================")
        print("🔥 NEW REQUEST")
        print("=========================")
        print("Content-Type:", request.content_type)

        # =========================
        # HANDLE BOTH JSON + FORMDATA
        # =========================
        if request.content_type and "multipart/form-data" in request.content_type:
            data = request.form.to_dict()
            file = request.files.get("file")
        else:
            data = request.get_json(silent=True) or {}
            file = None

        print("DATA:", data)
        print("FILE:", file.filename if file else "No file")

        # =========================
        # VALIDATION
        # =========================
        service = data.get("service_type")
        size = data.get("home_size")

        if not service or not size:
            return (
                jsonify(
                    {"success": False, "error": "Missing service_type or home_size"}
                ),
                400,
            )

        # =========================
        # PRICING ENGINE
        # =========================
        base_prices = {"air_duct": 150, "dryer_vent": 120, "carpet": 100, "tile": 130}

        size_multiplier = {"small": 1, "medium": 1.5, "large": 2}

        base = base_prices.get(service, 100)
        multiplier = size_multiplier.get(size, 1)

        quote_cents = int(base * multiplier * 100)
        quote_dollars = round(quote_cents / 100, 2)

        # =========================
        # LEAD TIER
        # =========================
        if quote_cents > 25000:
            tier = "hot"
        elif quote_cents > 15000:
            tier = "warm"
        else:
            tier = "cold"

        # =========================
        # ✅ OPTIONAL: SEND SMS (TWILIO)
        # =========================
        if TWILIO_ENABLED:
            try:
                client = Client(
                    os.environ.get("TWILIO_ACCOUNT_SID"),
                    os.environ.get("TWILIO_AUTH_TOKEN"),
                )

                message = f"""
New Lead 🚀
Service: {service}
Size: {size}
Quote: ${quote_dollars}

Name: {data.get('name')}
Phone: {data.get('phone')}
ZIP: {data.get('zip')}
"""

                client.messages.create(
                    body=message,
                    from_=os.environ.get("TWILIO_NUMBER"),
                    to=os.environ.get("YOUR_PHONE_NUMBER"),
                )

                print("✅ SMS SENT")

            except Exception as sms_error:
                print("⚠️ SMS ERROR:", str(sms_error))
        else:
            print("ℹ️ Twilio not configured — skipping SMS")

        # =========================
        # RESPONSE
        # =========================
        response = {
            "success": True,
            "estimated_quote": quote_dollars,
            "quote": quote_dollars,
            "lead_tier": tier,
        }

        print("RESPONSE:", response)

        return jsonify(response), 200

    except Exception as e:
        print("❌ SERVER ERROR:", str(e))

        return jsonify({"success": False, "error": "Server error"}), 500


# =========================================
# RUN SERVER
# =========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)
