"""Phase 1 integration: one mock incident flows end-to-end.

payment -> incident row -> agent investigates -> decision JSON validates -> shown via API.
Covers Day 7 acceptance: 'one simulated payment → incident row → agent output → shown in UI'.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import backend.app.db as dbmod
from backend.app import models
from backend.app.main import app
from agents.investigator import investigate
from agents.schemas import DecisionOutput

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
models.Base.metadata.create_all(bind=engine)

def _override():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[dbmod.get_db] = _override
client = TestClient(app)

def test_one_mock_incident_end_to_end():
    sid = client.post("/suppliers", json={"name": "Phase1 Demo Co"}).json()["id"]
    pay = client.post("/payments", json={
        "supplier_id": sid, "amount": 12500.0, "invoice_no": "INV-2026-001",
        "po_no": "PO-7781", "idempotency_key": "phase1-demo-1"}).json()
    inc = client.post("/incidents", json={
        "payment_id": pay["id"], "type": "UNKNOWN_STATUS",
        "priority": "P1", "summary": "appears failed, original status ambiguous"}).json()

    decision = investigate(inc["id"], pay["id"], sid, 12500.0, "INV-2026-001", "PO-7781")
    assert isinstance(decision, DecisionOutput)
    assert decision.action in ("WAIT", "REPLACE", "ESCALATE")
    assert decision.confidence < 0.80  # ambiguous mock -> escalate path
    assert decision.action == "ESCALATE"
    assert len(decision.reasoning_summary) >= 10

    # incident still retrievable ("shown in UI" via GET)
    fetched = client.get(f"/incidents/{inc['id']}").json()
    assert fetched["id"] == inc["id"]
    assert fetched["payment_id"] == pay["id"]
