"""Simulator runner (P4 Day 6): publishes payment+incident events to the bus.

Usage:
    python -m simulator.run --scenario 3
    python -m simulator.run --scenario 3 --api http://localhost:8000  (creates real rows)
"""
import argparse
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from simulator.scenarios import get
from simulator.event_generator import timeline
from simulator.bank import query

def run(scenario_n: int, api: str = "") -> dict:
    sc = get(scenario_n)
    payment_id = f"pay-sim-s{scenario_n}"
    incident_id = f"inc-sim-s{scenario_n}"
    print(f"[sim] scenario {scenario_n}: {sc['name']} — {sc['desc']}")
    for e in timeline(sc["bank"]):
        print(f"  event {e['type']}: {e['summary']}")
    print(f"  bank query -> {query(payment_id, sc['bank'])}")
    print(f"  expected agent decision: {sc['expected']}")

    # publish to bus (redis or in-memory) so backend/UI can observe
    try:
        from backend.app.events import publish_event
        eid = publish_event("payments", {"payment_id": payment_id, "scenario": sc["name"]})
        publish_event("incidents", {"incident_id": incident_id, "payment_id": payment_id})
        print(f"  bus publish ok ({eid})")
    except Exception as ex:
        print(f"  bus publish skipped: {ex}")

    if api:
        import httpx
        sid = httpx.post(f"{api}/suppliers", json={"name": "Sim Supplier"}).json()["id"]
        pay = httpx.post(f"{api}/payments", json={
            "supplier_id": sid, "amount": 12500.0, "invoice_no": "INV-SIM-003",
            "po_no": "PO-SIM-3", "idempotency_key": f"sim-s{scenario_n}"}).json()
        inc = httpx.post(f"{api}/incidents", json={
            "payment_id": pay["id"], "type": "UNKNOWN_STATUS" if scenario_n in (3, 5) else "OVERDUE",
            "priority": "P1" if scenario_n == 3 else "P2",
            "summary": f"Sim scenario {scenario_n}: {sc['name']}"}).json()
        print(f"  api rows: payment={pay['id']} incident={inc['id']}")
        return {"payment_id": pay["id"], "incident_id": inc["id"], "scenario": sc}
    return {"payment_id": payment_id, "incident_id": incident_id, "scenario": sc}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", type=int, default=3)
    ap.add_argument("--api", type=str, default="")
    a = ap.parse_args()
    print(run(a.scenario, a.api))
