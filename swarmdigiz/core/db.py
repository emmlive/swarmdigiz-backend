import sqlite3
import os
import bcrypt

# =========================================================
# DATABASE PATH
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "swarmdigiz.db")

if os.getenv("RAILWAY_ENVIRONMENT"):
    DB_PATH = "/data/swarmdigiz.db"
else:
    DB_PATH = DEFAULT_DB_PATH


# =========================================================
# DATABASE CONNECTION
# =========================================================


def get_connection():

    print(f"🔥 USING DB PATH: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")

    return conn


# =========================================================
# VERIFY SCHEMA VERSION
# =========================================================


def verify_schema_version():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_version (
            id INTEGER PRIMARY KEY,
            version INTEGER
        )
    """
    )

    cur.execute("SELECT version FROM schema_version WHERE id = 1")
    row = cur.fetchone()

    if not row:
        cur.execute("INSERT INTO schema_version (id, version) VALUES (1, 1)")
        conn.commit()

    conn.close()


# =========================================================
# ENSURE REQUIRED TABLES (FAILSAFE)
# =========================================================


def ensure_required_tables():

    conn = get_connection()
    cur = conn.cursor()

    # SERVICES
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER,
            name TEXT,
            base_price REAL,
            config TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    cur.execute("PRAGMA table_info(services)")
    service_cols = [c[1] for c in cur.fetchall()]

    if "name" not in service_cols:
        cur.execute("ALTER TABLE services ADD COLUMN name TEXT")

    if "base_price" not in service_cols:
        cur.execute("ALTER TABLE services ADD COLUMN base_price REAL")

    if "config" not in service_cols:
        cur.execute("ALTER TABLE services ADD COLUMN config TEXT")

    if "created_at" not in service_cols:
        cur.execute(
            "ALTER TABLE services ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        )

    # BOOKINGS
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER,
            lead_id INTEGER,
            customer_name TEXT,
            service TEXT,
            scheduled_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    cur.execute("PRAGMA table_info(bookings)")
    booking_cols = [c[1] for c in cur.fetchall()]

    if "business_id" not in booking_cols:
        cur.execute("ALTER TABLE bookings ADD COLUMN business_id INTEGER")

    if "lead_id" not in booking_cols:
        cur.execute("ALTER TABLE bookings ADD COLUMN lead_id INTEGER")

    if "customer_name" not in booking_cols:
        cur.execute("ALTER TABLE bookings ADD COLUMN customer_name TEXT")

    if "service" not in booking_cols:
        cur.execute("ALTER TABLE bookings ADD COLUMN service TEXT")

    if "scheduled_date" not in booking_cols:
        cur.execute("ALTER TABLE bookings ADD COLUMN scheduled_date TEXT")

    if "created_at" not in booking_cols:
        cur.execute(
            "ALTER TABLE bookings ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        )

    # CONNECTOR LOGS (critical for analytics)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS connector_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER,
            connector_type TEXT,
            payload TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    cur.execute("PRAGMA table_info(connector_logs)")
    connector_cols = [c[1] for c in cur.fetchall()]

    if "business_id" not in connector_cols:
        cur.execute("ALTER TABLE connector_logs ADD COLUMN business_id INTEGER")

    if "connector_type" not in connector_cols:
        cur.execute("ALTER TABLE connector_logs ADD COLUMN connector_type TEXT")

    if "payload" not in connector_cols:
        cur.execute("ALTER TABLE connector_logs ADD COLUMN payload TEXT")

    if "created_at" not in connector_cols:
        cur.execute(
            "ALTER TABLE connector_logs ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        )

    # SWARM RUNS (critical for run history / analytics)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS swarm_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            business_id INTEGER,
            goal TEXT,
            mode TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    cur.execute("PRAGMA table_info(swarm_runs)")
    swarm_cols = [c[1] for c in cur.fetchall()]

    if "username" not in swarm_cols:
        cur.execute("ALTER TABLE swarm_runs ADD COLUMN username TEXT")

    if "business_id" not in swarm_cols:
        cur.execute("ALTER TABLE swarm_runs ADD COLUMN business_id INTEGER")

    if "goal" not in swarm_cols:
        cur.execute("ALTER TABLE swarm_runs ADD COLUMN goal TEXT")

    if "mode" not in swarm_cols:
        cur.execute("ALTER TABLE swarm_runs ADD COLUMN mode TEXT")

    if "created_at" not in swarm_cols:
        cur.execute(
            "ALTER TABLE swarm_runs ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        )

    conn.commit()
    conn.close()


# =========================================================
# INITIALIZE DATABASE
# =========================================================


def initialize_database():

    conn = get_connection()
    cur = conn.cursor()

    # =====================================================
    # USERS
    # =====================================================

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            password_hash TEXT,
            business_id INTEGER,
            subscription_status TEXT DEFAULT 'active'
        )
    """
    )

    cur.execute("PRAGMA table_info(users)")
    cols = [c[1] for c in cur.fetchall()]

    if "subscription_status" not in cols:
        cur.execute(
            "ALTER TABLE users ADD COLUMN subscription_status TEXT DEFAULT 'active'"
        )

    # =====================================================
    # BUSINESSES
    # =====================================================

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS businesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            name TEXT
        )
    """
    )

    # =====================================================
    # INSPECTION RUNS (FULL HARDENED)
    # =====================================================

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS inspection_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            business_id INTEGER,
            service_type TEXT,
            lead_score INTEGER,
            lead_tier TEXT,
            booking_status TEXT DEFAULT 'new',
            estimated_quote REAL,
            estimated_revenue REAL,
            image_path TEXT,
            payload TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    cur.execute("PRAGMA table_info(inspection_runs)")
    cols = [c[1] for c in cur.fetchall()]

    required_columns = {
        "username": "TEXT",
        "business_id": "INTEGER",
        "service_type": "TEXT",
        "lead_score": "INTEGER",
        "lead_tier": "TEXT",
        "booking_status": "TEXT DEFAULT 'new'",
        "estimated_quote": "REAL",
        "estimated_revenue": "REAL",
        "image_path": "TEXT",
        "payload": "TEXT",
    }

    for col, col_type in required_columns.items():
        if col not in cols:
            cur.execute(f"ALTER TABLE inspection_runs ADD COLUMN {col} {col_type}")

    # =====================================================
    # SWARM RUNS
    # =====================================================

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS swarm_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            business_id INTEGER,
            goal TEXT,
            mode TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # =====================================================
    # CONNECTOR LOGS
    # =====================================================

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS connector_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER,
            connector_type TEXT,
            payload TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # =====================================================
    # GUARANTEE CRITICAL TABLES EXIST
    # =====================================================

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS connector_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER,
            connector_type TEXT,
            payload TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS swarm_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            business_id INTEGER,
            goal TEXT,
            mode TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # =====================================================
    # DEFAULT ADMIN
    # =====================================================

    cur.execute("SELECT id FROM users WHERE username = 'admin'")
    admin = cur.fetchone()

    if not admin:
        password_hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()

        cur.execute(
            """
            INSERT INTO users
            (username, email, password_hash, business_id, subscription_status)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                "admin",
                "admin@swarmdigiz.com",
                password_hash,
                1,
                "active",
            ),
        )

    conn.commit()
    conn.close()

    ensure_required_tables()
