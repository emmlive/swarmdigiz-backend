import stripe
import os
import uuid

from core.db import get_connection

# =========================================================
# STRIPE CONFIG
# =========================================================

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

if not stripe.api_key:
    raise Exception("STRIPE_SECRET_KEY not set in environment")


# =========================================================
# GET OR CREATE STRIPE CUSTOMER
# =========================================================


def get_or_create_customer(username: str, business_name: str):

    conn = get_connection()
    cur = conn.cursor()

    # Check existing customer
    cur.execute(
        """
        SELECT stripe_customer_id
        FROM stripe_customers
        WHERE username = ?
        """,
        (username,),
    )

    row = cur.fetchone()

    if row:
        conn.close()
        return row[0]

    # Create Stripe customer
    customer = stripe.Customer.create(
        name=business_name, metadata={"username": username}
    )

    customer_id = customer.id

    # Save locally
    cur.execute(
        """
        INSERT INTO stripe_customers (id, username, stripe_customer_id)
        VALUES (?, ?, ?)
        """,
        (str(uuid.uuid4()), username, customer_id),
    )

    conn.commit()
    conn.close()

    return customer_id


# =========================================================
# CREATE CHECKOUT SESSION
# =========================================================


def create_checkout_session(customer_id: str, price_id: str):

    session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        mode="subscription",
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        success_url="http://localhost:8501?success=true",
        cancel_url="http://localhost:8501?cancelled=true",
    )

    return session.url


# =========================================================
# UPDATE SUBSCRIPTION STATUS
# =========================================================


def update_subscription(customer_id: str, status: str, plan: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE stripe_customers
        SET subscription_status = ?, plan = ?
        WHERE stripe_customer_id = ?
        """,
        (status, plan, customer_id),
    )

    conn.commit()
    conn.close()
