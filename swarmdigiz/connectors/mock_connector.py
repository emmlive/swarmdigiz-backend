# ============================================================
# SwarmDigiz — Mock Connector
# Safe test connector (no external API calls)
# ============================================================

from datetime import datetime
from typing import Dict, Any
from connectors.base_connector import BaseConnector, ConnectorResponse


class MockConnector(BaseConnector):

    name = "mock"

    def execute(self, structured_payload: Dict[str, Any]) -> ConnectorResponse:
        # ------------------------------------------------------
        # Validate payload structure
        # ------------------------------------------------------
        self.validate(structured_payload)

        schema_version = structured_payload.get("schema_version")
        business_name = structured_payload.get("business_name")
        agents = structured_payload.get("agents", [])

        agent_count = len(agents)

        if agent_count == 0:
            return ConnectorResponse(
                success=False,
                message="Mock connector received no agents to process.",
                metadata={
                    "processed_agents": 0,
                    "business_name": business_name,
                    "schema_version": schema_version,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

        # ------------------------------------------------------
        # Simulated processing
        # ------------------------------------------------------
        return ConnectorResponse(
            success=True,
            message=f"Mock connector processed {agent_count} agents successfully.",
            metadata={
                "processed_agents": agent_count,
                "business_name": business_name,
                "schema_version": schema_version,
                "timestamp": datetime.utcnow().isoformat()
            }
        )