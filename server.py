from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# ✅ Enable CORS
CORS(app)


# =========================================
# HEALTH CHECK
# =========================================
@app.route("/")
def home():
    return "API is running"


# =========================================
# INSPECTION ENDPOINT (FIXED)
# =========================================
@app.route("/api/inspection", methods=["POST"])
def inspection():
    try:
        print("\n--- NEW REQUEST ---")
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
        print("FILE:", file)

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

        # ✅ keep cents for backend logic
        quote_cents = int(base * multiplier * 100)

        # ✅ convert for frontend display
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
        # RESPONSE (STANDARDIZED)
        # =========================
        response = {
            "success": True,
            "estimated_quote": quote_dollars,  # ✅ PRIMARY FIELD
            "quote": quote_dollars,  # ✅ fallback compatibility
            "lead_tier": tier,
        }

        print("RESPONSE:", response)

        return jsonify(response), 200

    except Exception as e:
        print("ERROR:", str(e))

        return jsonify({"success": False, "error": "Server error"}), 500


# =========================================
# RUN SERVER
# =========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
