# -*- coding: utf-8 -*-

import stripe

from core.stripe_config import stripe


def create_checkout_session(customer_email):

    session = stripe.checkout.Session.create(

        payment_method_types=["card"],

        mode="subscription",

        line_items=[
            {
                "price_data": {

                    "currency": "usd",

                    "product_data": {
                        "name": "SwarmDigiz Pro"
                    },

                    "unit_amount": 9900,  # $99/month

                    "recurring": {
                        "interval": "month"
                    }

                },

                "quantity": 1
            }
        ],

        success_url="http://localhost:8501?payment=success",

        cancel_url="http://localhost:8501?payment=cancel",

        customer_email=customer_email

    )

    return session.url