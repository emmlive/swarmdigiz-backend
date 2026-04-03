# ============================================================
# SwarmDigiz — Connector Abstraction Layer
# Base Connector Interface
# ============================================================

from typing import Dict, Any


class ConnectorResponse:
    def __init__(self, success: bool, message: str, metadata: Dict[str, Any] = None):
        self.success = success
        self.message = message
        self.metadata = metadata or {}

    def to_dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "metadata": self.metadata
        }


class BaseConnector:
    """
    All connectors must inherit from this class.
    """

    name = "base"

    def validate(self, structured_payload: Dict[str, Any]) -> bool:
        """
        Validate payload before execution.
        """
        required_fields = ["schema_version", "business_name", "agents"]

        for field in required_fields:
            if field not in structured_payload:
                raise ValueError(f"Missing required field: {field}")

        return True

    def execute(self, structured_payload: Dict[str, Any]) -> ConnectorResponse:
        """
        Must be implemented by subclass.
        """
        raise NotImplementedError("Connector must implement execute()")