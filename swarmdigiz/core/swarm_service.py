import json
from core.db import get_connection


# =========================================================
# CREATE SWARM RUN
# =========================================================

def create_swarm_run(username, metadata, business_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO swarm_runs (username, business_id, metadata)
        VALUES (?, ?, ?)
        """,
        (
            username,
            business_id,
            json.dumps(metadata)
        )
    )

    run_id = cur.lastrowid

    conn.commit()
    conn.close()

    return run_id


# =========================================================
# SAVE SWARM OUTPUT
# =========================================================

def save_swarm_output(run_id, agent_name, output_text):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO swarm_outputs (run_id, agent_name, output_text)
        VALUES (?, ?, ?)
        """,
        (
            run_id,
            agent_name,
            output_text
        )
    )

    conn.commit()
    conn.close()


# =========================================================
# LOAD SWARM OUTPUTS
# =========================================================

def load_swarm_outputs(run_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT agent_name, output_text
        FROM swarm_outputs
        WHERE run_id = ?
        """,
        (run_id,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows


# =========================================================
# LIST SWARM RUNS
# =========================================================

def list_swarm_runs(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, username, created_at
        FROM swarm_runs
        WHERE username = ?
        ORDER BY created_at DESC
        """,
        (username,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows


# =========================================================
# GET RUN METADATA
# =========================================================

def get_run_metadata(run_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT metadata
        FROM swarm_runs
        WHERE id = ?
        """,
        (run_id,)
    )

    row = cur.fetchone()

    conn.close()

    if not row:
        return None

    return json.loads(row[0])