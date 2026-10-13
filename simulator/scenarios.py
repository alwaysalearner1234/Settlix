"""5 scenarios (P4 Day 4 skeleton; full logic Phase 2/3). Scenario 3 is the hero demo."""
SCENARIOS = {
    1: {"name": "normal_delay", "bank": "normal_delay", "expected": "WAIT",
        "desc": "Bank slow but healthy; agent should WAIT and recheck."},
    2: {"name": "confirmed_failure", "bank": "confirmed_failure", "expected": "REPLACE",
        "desc": "Bank confirms failure; duplicate check passes; safe to REPLACE."},
    3: {"name": "dangerous_unknown", "bank": "dangerous_unknown", "expected": "ESCALATE",
        "desc": "HERO: original may still settle. Duplicate REPLACE would double-pay. Must ESCALATE."},
    4: {"name": "returned", "bank": "returned", "expected": "REPLACE",
        "desc": "Funds returned; safe to re-issue after guard passes."},
    5: {"name": "ambiguous", "bank": "ambiguous", "expected": "ESCALATE",
        "desc": "Conflicting signals, 54% confidence; must ESCALATE for human review."},
}

def get(n: int) -> dict:
    return SCENARIOS[n]
