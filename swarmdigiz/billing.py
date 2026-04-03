
import stripe
import sqlite3
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

AGENT_PRICING = {
    "analyst": 1,
    "ads": 2,
    "seo": 2,
    "creative": 3,
    "strategist": 2
}

def db(db_path):
    return sqlite3.connect(db_path, check_same_thread=False)

def get_agent_cost(agent):
    return AGENT_PRICING.get(agent, 1)

def charge_credits(db_path, username, amount):
    conn = db(db_path)
    cur = conn.cursor()
    cur.execute("SELECT credits FROM users WHERE username=?", (username,))
    credits = cur.fetchone()[0]
    if credits < amount:
        conn.close()
        raise Exception("Insufficient credits")
    cur.execute("UPDATE users SET credits=credits-? WHERE username=?", (amount, username))
    conn.commit()
    conn.close()

def stripe_topup(username, amount, db_path):
    intent = stripe.PaymentIntent.create(
        amount=int(amount * 100),
        currency="usd",
        automatic_payment_methods={"enabled": True}
    )
    conn = db(db_path)
    conn.execute("UPDATE users SET credits=credits+? WHERE username=?", (int(amount), username))
    conn.commit()
    conn.close()
    return intent.client_secret
