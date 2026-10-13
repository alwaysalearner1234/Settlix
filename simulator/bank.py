"""Simulated bank behaviours (P4 Day 3). Deterministic per scenario."""
from typing import Dict, Any

def query(payment_id: str, scenario: str) -> Dict[str, Any]:
    behaviours = {
        "normal_delay": {"status": "PENDING", "latency_ms": 800, "note": "bank slow, will settle"},
        "confirmed_failure": {"status": "FAILED", "code": "NSF_ROUTE", "note": "bank rejected"},
        "dangerous_unknown": {"status": "UNKNOWN", "note": "timeout, original may still settle — DO NOT duplicate blindly"},
        "returned": {"status": "RETURNED", "note": "funds returned to sender"},
        "ambiguous": {"status": "UNKNOWN", "latency_ms": 5000, "note": "conflicting signals"},
    }
    return {"payment_id": payment_id, **behaviours.get(scenario, behaviours["ambiguous"])}
