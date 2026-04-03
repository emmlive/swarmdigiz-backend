import stripe
import os

# =========================================================
# CONFIG
# =========================================================

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501")

if not STRIPE_SECRET_KEY:
    print("⚠️ WARNING: STRIPE_SECRET_KEY not set")

stripe.api_key = STRIPE_SECRET_KEY


# =========================================================
# CREATE PAYMENT INTENT (LEGACY / OPTIONAL)
# =========================================================

def create_payment_intent(amount_cents: int, metadata: dict = None):
    """
    Creates a Stripe PaymentIntent

    amount_cents: integer (e.g. $100 → 10000)
    metadata: optional dict (tier, service, user, etc.)
    """

    try:
        if amount_cents <= 0:
            raise ValueError("Amount must be greater than 0")

        intent = stripe.PaymentIntent.create(
            amount=int(amount_cents),
            currency="usd",
            automatic_payment_methods={"enabled": True},
            metadata=metadata or {},
        )

        return {
            "success": True,
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# CREATE CHECKOUT SESSION (PRIMARY FLOW)
# =========================================================

def create_checkout_session(amount_cents: int, metadata: dict = None):
    """
    Creates a Stripe Hosted Checkout Session
    """

    try:
        if amount_cents <= 0:
            raise ValueError("Amount must be greater than 0")

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Service Booking",
                        },
                        "unit_amount": int(amount_cents),
                    },
                    "quantity": 1,
                }
            ],
            success_url=f"{FRONTEND_URL}?payment=success",
            cancel_url=f"{FRONTEND_URL}?payment=cancel",
            metadata=metadata or {},
        )

        return {
            "success": True,
            "checkout_url": session.url,
            "session_id": session.id,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# DEPOSIT CALCULATION
# =========================================================

def calculate_deposit(total_amount: int):
    """
    Returns a safe deposit amount (30% default)
    Enforces minimum charge of $25
    """

    try:
        if total_amount <= 0:
            return 25

        deposit = int(round(total_amount * 0.3))

        return max(deposit, 25)

    except Exception:
        return 25


# =========================================================
# BUILD PAYMENT OPTIONS
# =========================================================

def build_payment_options(total_amount: int):
    """
    Builds full + deposit payment options
    """

    try:
        total_amount = int(total_amount)
        deposit = calculate_deposit(total_amount)

        return {
            "full": {
                "label": "Pay in Full",
                "amount": total_amount,
                "type": "full"
            },
            "deposit": {
                "label": "Reserve with Deposit",
                "amount": deposit,
                "type": "deposit"
            }
        }

    except Exception:
        return {
            "full": {
                "label": "Pay in Full",
                "amount": total_amount,
                "type": "full"
            }
        }