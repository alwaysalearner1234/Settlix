"""API tests — payments/suppliers/incidents + idempotency (P4 Day 5/11 skeleton)."""
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import backend.app.db as dbmod
from backend.app import models
from backend.app.main import app

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
models.Base.metadata.create_all(bind=engine)

def override_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[dbmod.get_db] = override_db
client = TestClient(app)

def test_health():
    assert client.get("/health").json()["status"] == "ok"

def test_payment_idempotent_create():
    sid = client.post("/suppliers", json={"name": "TestCo"}).json()["id"]
    key = f"k-{uuid.uuid4().hex[:8]}"
    b1 = client.post("/payments", json={"supplier_id": sid, "amount": 100.0,
                                        "invoice_no": "INV-T1", "idempotency_key": key}).json()
    b2 = client.post("/payments", json={"supplier_id": sid, "amount": 100.0,
                                        "invoice_no": "INV-T1", "idempotency_key": key}).json()
    assert b1["id"] == b2["id"]

def test_incident_flow():
    sid = client.post("/suppliers", json={"name": "FlowCo"}).json()["id"]
    pay = client.post("/payments", json={"supplier_id": sid, "amount": 500.0,
                                         "invoice_no": "INV-F1",
                                         "idempotency_key": f"k-{uuid.uuid4().hex[:8]}"}).json()
    inc = client.post("/incidents", json={"payment_id": pay["id"], "type": "OVERDUE"}).json()
    assert inc["payment_id"] == pay["id"]
    got = client.get(f"/incidents/{inc['id']}").json()
    assert got["id"] == inc["id"]
