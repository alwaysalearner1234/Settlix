"""Payment state machine + transition tests target (P2 Day 3)."""
from typing import Dict, List

STATES = ["INITIATED", "PENDING", "SETTLED", "FAILED", "RETURNED", "UNKNOWN"]

ALLOWED: Dict[str, List[str]] = {
    "INITIATED": ["PENDING", "FAILED"],
    "PENDING": ["SETTLED", "FAILED", "RETURNED", "UNKNOWN"],
    "UNKNOWN": ["SETTLED", "FAILED", "RETURNED", "PENDING"],
    "FAILED": ["PENDING"],  # only via replacement retry, guarded
    "RETURNED": ["PENDING"],
    "SETTLED": [],  # terminal — replacement from SETTLED is a duplicate, must block
}

class IllegalTransition(Exception):
    pass

def transition(current: str, nxt: str) -> str:
    if nxt not in ALLOWED.get(current, []):
        raise IllegalTransition(f"{current} -> {nxt} not allowed")
    return nxt

def is_terminal(status: str) -> bool:
    return status in ("SETTLED",)
