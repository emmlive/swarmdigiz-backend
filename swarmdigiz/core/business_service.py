from core.db import get_connection


def get_or_create_business(username, business_name):

    conn = get_connection()
    cur = conn.cursor()

    # ======================================
    # CHECK EXISTING BUSINESS
    # ======================================

    cur.execute(
        """
        SELECT id
        FROM businesses
        WHERE username = ? AND name = ?
        """,
        (username, business_name)
    )

    row = cur.fetchone()

    if row:
        conn.close()
        return row[0]

    # ======================================
    # CREATE BUSINESS
    # ======================================

    cur.execute(
        """
        INSERT INTO businesses (username, name)
        VALUES (?, ?)
        """,
        (username, business_name)
    )

    business_id = cur.lastrowid

    conn.commit()
    conn.close()

    return business_id