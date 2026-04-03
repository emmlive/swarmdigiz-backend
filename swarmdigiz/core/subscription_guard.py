from core.db import get_connection


def verify_subscription(username):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT subscription_status
    FROM users
    WHERE username = ?
    """, (username,))

    row = cur.fetchone()

    conn.close()

    if not row:
        return False

    return row[0] == "active"