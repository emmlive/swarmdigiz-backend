# -*- coding: utf-8 -*-

import bcrypt
from datetime import datetime
from core.db import get_connection


# ---------------------------------------------------------
# CREATE USER
# ---------------------------------------------------------

def create_user(username, email, password, business_id):

    conn = get_connection()
    cur = conn.cursor()

    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()  # store as string

    cur.execute("""
    INSERT INTO users
    (username, email, password_hash, business_id)
    VALUES (?, ?, ?, ?)
    """, (
        username,
        email,
        password_hash,
        business_id
    ))

    conn.commit()
    conn.close()


# ---------------------------------------------------------
# VERIFY LOGIN
# ---------------------------------------------------------

def verify_user(username, password):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT password_hash, business_id
    FROM users
    WHERE username = ?
    """, (username,))

    row = cur.fetchone()

    conn.close()

    if not row:
        return None

    password_hash = row["password_hash"]
    business_id = row["business_id"]

    # Convert stored hash to bytes for bcrypt
    if isinstance(password_hash, str):
        password_hash = password_hash.encode()

    if bcrypt.checkpw(password.encode(), password_hash):
        return business_id

    return None