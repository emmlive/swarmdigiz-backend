# core/stripe_config.py

import stripe

# Replace with your real Stripe secret key
import os

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
