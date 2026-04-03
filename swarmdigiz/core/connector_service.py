from core.db import get_connection
import json
from datetime import datetime


# =========================================================
# LOG CONNECTOR EXECUTION
# =========================================================

def log_connector_execution(
    business_id,
    connector_type,
    payload,
    response_status="success"
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO connector_logs
        (
            business_id,
            connector_type,
            payload,
            response_status,
            executed_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            business_id,
            connector_type,
            json.dumps(payload),
            response_status,
            datetime.utcnow()
        )
    )

    conn.commit()
    conn.close()