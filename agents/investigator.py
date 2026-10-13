"""First agent loop on mocks (P1 Day 5) -> real tools via API (P1 Day 6).

Phase 1: deterministic rule-based reasoning (no LLM key required).
Phase 3: swap _reason() for a Bedrock/LLM call returning DecisionOutput.
Safety Engine (Phase 2) validates the output before any financial action.
"""
from datetime import datetime, timedelta
from . import tools
from .evidence import aggregate
from .schemas import DecisionOutput, EvidenceRef, DuplicateRisk

def investigate(incident_id: str, payment_id: str, supplier_id: str = "sup-mock",
                amount: float = 12500.0, invoice_no: str = "INV-2026-001",
                po_no: str = "PO-7781") -> DecisionOutput:
    calls = [
        tools.get_payment_status(payment_id),
        tools.get_payment_events(payment_id),
        tools.get_failure_reason(payment_id),
        tools.get_bank_statement(payment_id),
        tools.check_duplicate(supplier_id, amount, invoice_no, po_no),
        tools.get_supplier_history(supplier_id),
    ]
    evidence = aggregate(calls)
    conf = tools.estimate_confidence(evidence)

    bank_status = evidence.get("get_bank_statement", {}).get("bank", {}).get("status", "UNKNOWN")
    dup = evidence.get("check_duplicate", {}).get("duplicate", {})

    if dup.get("is_duplicate_risk"):
        action, conf = "ESCALATE", min(conf, 0.6)
        summary = (f"Duplicate risk on {invoice_no}: matched {dup.get('matched_on')}. "
                   f"Blocked replacement to avoid double-pay; escalated for human review.")
    elif bank_status == "UNKNOWN" or conf < 0.80:
        action = "ESCALATE"
        summary = (f"Payment {payment_id[:8]} status ambiguous (bank={bank_status}, no ack within SLA). "
                   f"Confidence {conf:.0%} below 0.80 threshold; escalated for human review. "
                   f"Duplicate check passed; no replacement issued.")
    elif bank_status == "FAILED":
        action, summary = "REPLACE", "Bank confirmed failure; duplicate check passed; replacement proposed."
    else:
        action, summary = "WAIT", "Brief delay, bank pending; recheck scheduled."

    ev_refs = [EvidenceRef(tool=c.get("tool", "unknown"), summary=str(c)[:200]) for c in calls]
    nxt = (datetime.utcnow() + timedelta(hours=4)).isoformat() if action == "WAIT" else None
    return DecisionOutput(
        incident_id=incident_id, action=action, confidence=round(float(conf), 2),
        reasoning_summary=summary, evidence=ev_refs, next_check_at=nxt,
        duplicate_risk=DuplicateRisk(is_duplicate_risk=bool(dup.get("is_duplicate_risk")),
                                     matched_on=list(dup.get("matched_on", [])),
                                     existing_payment_id=dup.get("existing_payment_id")),
        rule_version="safety-v1",
    )

if __name__ == "__main__":
    import json
    print(json.dumps(investigate("inc-demo", "pay-demo").model_dump(), indent=2))
