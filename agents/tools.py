"""10 agent tools — mock mode default (Phase 1), real mode via backend API (P1 Day 2/8).

Mock data is deterministic so the Phase 1 demo and CI pass without Postgres/Redis/LLM.
Real mode: set SETTLIX_API=http://localhost:8000 and pass payment/incident ids from the DB.
"""
import os
from typing import Any, Dict, List

API = os.getenv("SETTLIX_API", "")
MOCK_BANK = {"status": "UNKNOWN", "latency_ms": 1200, "note": "no ack from bank yet"}

def _get(path: str) -> Any:
    if not API:
        return None
    import httpx
    r = httpx.get(f"{API}{path}", timeout=5.0)
    r.raise_for_status()
    return r.json()

def get_payment_status(payment_id: str) -> Dict[str, Any]:
    live = _get(f"/payments/{payment_id}") if API else None
    if live:
        return {"tool": "get_payment_status", "payment": live}
    return {"tool": "get_payment_status",
            "payment": {"id": payment_id, "status": "PENDING", "amount": 12500.0,
                        "supplier_id": "sup-mock", "due_at": "overdue-1h", "idempotency_key": "seed-mock"}}

def get_payment_events(payment_id: str) -> Dict[str, Any]:
    live = _get(f"/payments/{payment_id}/events") if API else None
    if live is not None:
        return {"tool": "get_payment_events", "events": live}
    return {"tool": "get_payment_events", "events": [
        {"type": "CREATED", "summary": "payment created"},
        {"type": "SENT", "summary": "sent via swift, awaiting bank ack"},
    ]}

def get_failure_reason(payment_id: str) -> Dict[str, Any]:
    return {"tool": "get_failure_reason",
            "failure": {"code": "NO_ACK", "message": "No bank acknowledgement within SLA", "retryable": True}}

def get_supplier_history(supplier_id: str, limit: int = 10) -> Dict[str, Any]:
    return {"tool": "get_supplier_history",
            "history": {"supplier_id": supplier_id, "past_payments": 24, "failures": 1, "failure_rate": 0.04}}

def get_similar_incidents(payment_id: str, limit: int = 5) -> Dict[str, Any]:
    return {"tool": "get_similar_incidents", "incidents": [
        {"id": "inc-prev-1", "resolution": "WAIT then settled after 6h"}]}

def check_duplicate(supplier_id: str, amount: float, invoice_no: str, po_no: str, window_hours: int = 72) -> Dict[str, Any]:
    """Duplicate Guard skeleton (P2 Day 10 full version lives in backend)."""
    return {"tool": "check_duplicate",
            "duplicate": {"is_duplicate_risk": False, "matched_on": [], "existing_payment_id": None,
                          "checked": {"supplier_id": supplier_id, "amount": amount,
                                      "invoice_no": invoice_no, "po_no": po_no, "window_hours": window_hours}}}

def get_bank_statement(payment_id: str) -> Dict[str, Any]:
    return {"tool": "get_bank_statement", "bank": MOCK_BANK}

def get_invoice_details(invoice_no: str) -> Dict[str, Any]:
    return {"tool": "get_invoice_details",
            "invoice": {"invoice_no": invoice_no, "po_no": "PO-7781", "amount_matches": True}}

def get_audit_trail(incident_id: str) -> Dict[str, Any]:
    return {"tool": "get_audit_trail", "trail": []}

def estimate_confidence(evidence: Dict[str, Any]) -> float:
    """Phase 1 heuristic: ambiguous bank status -> low confidence (forces ESCALATE path in hero demo)."""
    bank = ""
    try:
        bank = evidence.get("get_bank_statement", {}).get("bank", {}).get("status", "")
    except Exception:
        pass
    if bank == "UNKNOWN":
        return 0.54
    return 0.85

TOOLS = [get_payment_status, get_payment_events, get_failure_reason, get_supplier_history,
         get_similar_incidents, check_duplicate, get_bank_statement, get_invoice_details,
         get_audit_trail, estimate_confidence]
