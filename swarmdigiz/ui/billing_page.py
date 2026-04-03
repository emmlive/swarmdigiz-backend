# -*- coding: utf-8 -*-

import streamlit as st

from core.stripe_checkout import create_checkout_session


def render_billing_page():

    st.title("SwarmDigiz Subscription")

    st.markdown("### Upgrade to SwarmDigiz Pro")

    st.write("""
Pro Plan Includes:

• AI Visual Inspector  
• Marketing Swarm Automation  
• Campaign Launch Engine  
• Lead Pipeline  
• Growth Analytics
""")

    email = st.text_input("Business Email")

    if st.button("Start Subscription"):

        if not email:
            st.error("Email required")
            return

        checkout_url = create_checkout_session(email)

        st.markdown(f"[Click here to complete payment]({checkout_url})")