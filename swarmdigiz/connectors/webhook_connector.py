# ============================================================
# SwarmDigiz — Webhook Connector
# Sends structured payload to external endpoint via HTTP POST
# ============================================================

import requests
from typing import Dict, Any
from connectors.base_connector import BaseConnector, ConnectorResponse


class WebhookConnector(BaseConnector):

    name = "webhook"

    def __init__(self, endpoint_url: str, timeout: int = 10):
        self.endpoint_url = endpoint_url
        self.timeout = timeout

    def execute(self, structured_payload: Dict[str, Any]) -> ConnectorResponse:
        # Validate payload first
        self.validate(structured_payload)

        if not self.endpoint_url:
            return ConnectorResponse(
                success=False,
                message="Webhook endpoint URL not provided."
            )

        try:
            response = requests.post(
                self.endpoint_url,
                json=structured_payload,
                timeout=self.timeout,
                headers={
                    "Content-Type": "application/json"
                }
            )

            return ConnectorResponse(
                success=response.status_code in [200, 201, 202],
                message=f"Webhook responded with status {response.status_code}",
                metadata={
                    "status_code": response.status_code,
                    "response_text": response.text[:500]  # truncate for safety
                }
            )

        except requests.exceptions.RequestException as e:
            return ConnectorResponse(
                success=False,
                message="Webhook request failed.",
                metadata={"error": str(e)}
            )