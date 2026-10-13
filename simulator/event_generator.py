"""Event generator (P4 Day 4): builds timeline events per scenario."""
from datetime import datetime

def timeline(scenario: str) -> list[dict]:
    base = [
        {"type": "CREATED", "at": "t0", "summary": "payment created"},
        {"type": "SENT", "at": "t0+1m", "summary": "sent to bank"},
    ]
    extra = {
        "normal_delay": [{"type": "BANK_ACK_PENDING", "at": "t0+30m", "summary": "bank slow"}],
        "confirmed_failure": [{"type": "FAILED", "at": "t0+10m", "summary": "bank rejected: NSF_ROUTE"}],
        "dangerous_unknown": [{"type": "TIMEOUT", "at": "t0+60m", "summary": "ack timeout; original fate unknown"}],
        "returned": [{"type": "RETURNED", "at": "t0+2h", "summary": "funds returned"}],
        "ambiguous": [{"type": "TIMEOUT", "at": "t0+60m", "summary": "conflicting bank signals"}],
    }
    return base + extra.get(scenario, extra["ambiguous"])
