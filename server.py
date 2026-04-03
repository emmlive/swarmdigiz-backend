from flask import Flask
from flask_cors import CORS

# =========================================================
# IMPORT YOUR BACKEND MODULES
# =========================================================
from swarmdigiz.core.db import initialize_database, verify_schema_version
from swarmdigiz.api.inspection_api import inspection_bp

app = Flask(__name__)
CORS(app)

# =========================================================
# DATABASE INIT
# =========================================================
verify_schema_version()
initialize_database()

# =========================================================
# REGISTER ROUTES
# =========================================================
app.register_blueprint(inspection_bp)


# =========================================================
# HEALTH CHECK (RAILWAY USES THIS)
# =========================================================
@app.get("/")
def health():
    return {"status": "ok", "service": "swarmdigiz-api"}


# =========================================================
# ENTRY POINT
# =========================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
