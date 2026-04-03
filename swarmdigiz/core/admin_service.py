# -*- coding: utf-8 -*-

import sqlite3

DB_PATH = "swarmdigiz/swarmdigiz.db"


def list_users():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute(
            """
            SELECT username, subscription_status
            FROM users
            """
        )

        users = cur.fetchall()

    except:
        users = []

    conn.close()

    return users


def update_subscription(username, status):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET subscription_status = ?
        WHERE username = ?
        """,
        (status, username)
    )

    conn.commit()
    conn.close()