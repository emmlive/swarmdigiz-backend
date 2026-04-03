# -*- coding: utf-8 -*-

import streamlit as st


def render_embed_generator(business_id: int):

    st.title("🔗 Visual Inspector Embed Installer")

    st.markdown(
        """
Add the **AI Visual Inspector** to your website in minutes.

Copy the embed code below and paste it into your website.
"""
    )

    st.markdown("---")

    # ---------------------------------------------------------
    # Base URL
    # ---------------------------------------------------------

    base_url = st.text_input(
        "SwarmDigiz Platform URL",
        value="http://localhost:8501"
    )

    inspector_url = f"{base_url}?embed=true&business_id={business_id}"

    st.markdown("### Live Inspector URL")

    st.code(inspector_url)

    st.markdown("---")

    # ---------------------------------------------------------
    # Simple iFrame Embed
    # ---------------------------------------------------------

    iframe_code = f"""
<iframe
    src="{inspector_url}"
    width="100%"
    height="700"
    style="border:none;"
></iframe>
"""

    st.markdown("### Option 1 — Simple iFrame Embed")

    st.code(iframe_code, language="html")

    st.markdown(
        "Paste this code into your website page where you want the inspector to appear."
    )

    st.markdown("---")

    # ---------------------------------------------------------
    # Script Loader (Recommended)
    # ---------------------------------------------------------

    script_code = f"""
<div id="swarmdigiz-inspector"></div>

<script>
(function() {{
    var iframe = document.createElement("iframe");
    iframe.src = "{inspector_url}";
    iframe.style.width = "100%";
    iframe.style.height = "700px";
    iframe.style.border = "none";

    document.getElementById("swarmdigiz-inspector").appendChild(iframe);
}})();
</script>
"""

    st.markdown("### Option 2 — Script Installer (Recommended)")

    st.code(script_code, language="html")

    st.markdown(
        """
Add this script anywhere on your site and the inspector will load automatically.
"""
    )

    st.markdown("---")

    # ---------------------------------------------------------
    # Preview
    # ---------------------------------------------------------

    st.markdown("### Inspector Preview")

    st.components.v1.iframe(
        inspector_url,
        height=700
    )