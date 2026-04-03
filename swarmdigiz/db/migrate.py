import os
import sqlite3
import hashlib

# =========================================================
# PATH-SAFE CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DB_PATH = os.path.join(PROJECT_DIR, "swarmdigiz.db")
MIGRATIONS_DIR = os.path.join(BASE_DIR, "migrations")

# =========================================================
# SAFETY GUARD
# =========================================================

if os.getenv("ALLOW_SCHEMA_MUTATION") != "true":
    raise RuntimeError("❌ Schema mutation blocked (set ALLOW_SCHEMA_MUTATION=true)")

# =========================================================
# DB CONNECTION
# =========================================================

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# =========================================================
# BOOTSTRAP CORE TABLES
# =========================================================

cur.execute("""
CREATE TABLE IF NOT EXISTS migration_log (
    version INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    checksum TEXT NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS schema_version (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    version INTEGER NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cur.execute("SELECT COUNT(*) FROM schema_version")

if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO schema_version (id, version) VALUES (1, 0)")

conn.commit()

# =========================================================
# CHECKSUM
# =========================================================

def checksum(sql: str) -> str:
    return hashlib.sha256(sql.encode("utf-8")).hexdigest()

# =========================================================
# APPLY MIGRATIONS
# =========================================================

if not os.path.exists(MIGRATIONS_DIR):
    raise RuntimeError(f"❌ Migrations directory not found: {MIGRATIONS_DIR}")

files = sorted(
    f for f in os.listdir(MIGRATIONS_DIR)
    if f.endswith(".sql")
)

for file in files:

    version = int(file.split("_")[0])
    path = os.path.join(MIGRATIONS_DIR, file)

    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()

    hash_value = checksum(sql)

    cur.execute(
        "SELECT checksum FROM migration_log WHERE version = ?",
        (version,)
    )

    row = cur.fetchone()

    if row:
        if row[0] != hash_value:
            print(f"⚠️ Migration checksum mismatch for {file}, skipping")
        continue

    print(f"🚀 Applying migration {file}")

    try:

        cur.executescript(sql)

        cur.execute(
            "INSERT INTO migration_log (version, name, checksum) VALUES (?, ?, ?)",
            (version, file, hash_value)
        )

        cur.execute(
            "UPDATE schema_version SET version = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1",
            (version,)
        )

        conn.commit()

    except sqlite3.OperationalError as e:

        # duplicate column / already applied
        print(f"⚠️ Skipping migration {file}: {e}")

        conn.rollback()

        cur.execute(
            "INSERT OR IGNORE INTO migration_log (version, name, checksum) VALUES (?, ?, ?)",
            (version, file, hash_value)
        )

        conn.commit()

        continue

    except Exception as e:

        print(f"❌ Migration error in {file}: {e}")
        conn.rollback()
        continue

conn.close()

print("✅ Database is up to date")