"""Seed demo data — one supplier + one mock payment + overdue incident (Phase 1 Day 2/7)."""
import uuid
from datetime import datetime, timedelta
from .db import SessionLocal, init_db
from . import models

def seed():
    init_db()
    db = SessionLocal()
    try:
        if db.query(models.Supplier).count() == 0:
            s = models.Supplier(name="Acme Components Ltd", account_no="ACME-001", risk_score=0.2)
            db.add(s); db.commit(); db.refresh(s)
            print(f"supplier {s.id}")
        else:
            s = db.query(models.Supplier).first()
        key = f"seed-{uuid.uuid4().hex[:8]}"
        p = models.Payment(supplier_id=s.id, amount=12500.0, currency="USD",
                           invoice_no="INV-2026-001", po_no="PO-7781",
                           status="PENDING", idempotency_key=key,
                           due_at=datetime.utcnow() - timedelta(hours=1))
        db.add(p); db.commit(); db.refresh(p)
        db.add(models.PaymentEvent(payment_id=p.id, type="SENT", payload={"channel": "swift"}))
        inc = models.Incident(payment_id=p.id, type="OVERDUE", priority="P2",
                              summary="Seed: payment overdue, status ambiguous")
        db.add(inc)
        db.flush()
        db.add(models.AuditLog(incident_id=inc.id, actor="simulator", event="seed.created",
                               details={"payment_id": p.id}))
        db.commit()
        print(f"payment {p.id} incident {inc.id}")
        return {"supplier_id": s.id, "payment_id": p.id, "incident_id": inc.id}
    finally:
        db.close()

if __name__ == "__main__":
    print(seed())
