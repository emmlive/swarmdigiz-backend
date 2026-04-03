# ============================================================
# SwarmDigiz — Structured Output Builder
# Prepares swarm outputs for future connector integrations
# ============================================================

from datetime import datetime
from typing import Dict, Any, List


# ------------------------------------------------------------
# Content Type Mapping (Connector Preparation)
# ------------------------------------------------------------

AGENT_CONTENT_TYPE = {
    "Market Analyst": "research",
    "SEO Strategist": "seo",
    "Ad Copy Agent": "ad_copy",
    "Content Strategist": "blog",
    "Email Campaign Agent": "email",
    "Landing Page Architect": "landing_page",
    "Funnel Strategist": "funnel",
    "Brand Positioning Agent": "brand",
    "Offer Architect": "offer",
    "Social Media Strategist": "social"
}


# ------------------------------------------------------------
# Structured Builder
# ------------------------------------------------------------

def build_structured_output(
    business_name: str,
    raw_agents: List[Dict[str, Any]]
) -> Dict[str, Any]:

    structured_agents = []

    for agent in raw_agents:
        agent_name = agent.get("agent")
        content = agent.get("output")

        structured_agents.append({
            "agent_name": agent_name,
            "content_type": AGENT_CONTENT_TYPE.get(agent_name, "general"),
            "title": f"{agent_name} Output",
            "body": content,
            "connector_ready": True,
            "created_at": datetime.utcnow().isoformat()
        })

    return {
        "schema_version": "1.0",
        "business_name": business_name,
        "generated_at": datetime.utcnow().isoformat(),
        "agent_count": len(structured_agents),
        "agents": structured_agents
    }