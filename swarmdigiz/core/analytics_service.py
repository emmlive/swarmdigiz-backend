from core.db import db

def get_execution_analytics(username, run_id):
    conn = db()

    rows = conn.execute(
        """
        SELECT connector_name, success
        FROM connector_executions
        WHERE username=? AND run_id=?
        """,
        (username, run_id),
    ).fetchall()

    conn.close()

    total = len(rows)
    success_count = sum(1 for r in rows if r[1] == 1)
    failure_count = total - success_count

    breakdown = {}

    for connector_name, success in rows:

        if connector_name not in breakdown:
            breakdown[connector_name] = {
                "total": 0,
                "success": 0
            }

        breakdown[connector_name]["total"] += 1

        if success == 1:
            breakdown[connector_name]["success"] += 1

    return {
        "total": total,
        "success": success_count,
        "failure": failure_count,
        "breakdown": breakdown,
    }