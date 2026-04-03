from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# ✅ FIX: Enable CORS (CRITICAL)
CORS(app)


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
        data = request.get_json()

        service = data.get("service_type")
        size = data.get("home_size")

        base_prices = {"air_duct": 150, "dryer_vent": 120, "carpet": 100, "tile": 130}
        size_multiplier = {"small": 1, "medium": 1.5, "large": 2}

        base = base_prices.get(service, 100)
        multiplier = size_multiplier.get(size, 1)

        quote = int(base * multiplier * 100)

        if quote > 25000:
            tier = "hot"
        elif quote > 15000:
            tier = "warm"
        else:
            tier = "cold"

        return jsonify({"success": True, "quote": quote, "lead_tier": tier})

    except Exception as e:
        print("ERROR:", e)

        return jsonify({"success": False, "error": "Server error"}), 500


# =========================================
# RUN SERVER
# =========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
