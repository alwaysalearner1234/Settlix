"""Payments REST API (P2 Day 5). Idempotent create via idempotency_key."""
import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..events import publish_event

router = APIRouter(prefix="/payments", tags=["payments"])

def _out(p: models.Payment) -> dict:
    return {c.name: getattr(p, c.name) for c in p.__table__.columns}

@router.post("", response_model=schemas.PaymentOut)
def create_payment(body: schemas.PaymentIn, db: Session = Depends(get_db)):
    existing = db.query(models.Payment).filter_by(idempotency_key=body.idempotency_key).first()
    if existing:
        return _out(existing)
    sup = db.query(models.Supplier).filter_by(id=body.supplier_id).first()
    if not sup:
        raise HTTPException(404, "supplier not found")
    p = models.Payment(
        supplier_id=body.supplier_id, amount=body.amount, currency=body.currency,
        invoice_no=body.invoice_no, po_no=body.po_no, status="PENDING",
        idempotency_key=body.idempotency_key,
        due_at=datetime.utcnow() + timedelta(hours=body.due_hours),
    )
    db.add(p)
    db.flush()  # generate p.id before child rows
    db.add(models.PaymentEvent(payment_id=p.id, type="CREATED", payload={"amount": body.amount}))
    db.add(models.AuditLog(incident_id=None, actor="system", event="payment.created",
                           details={"payment_id": p.id, "idempotency_key": p.idempotency_key}))
    db.commit(); db.refresh(p)
    publish_event("payments", {"payment_id": p.id, "type": "CREATED"})
    return _out(p)

@router.get("", response_model=list[schemas.PaymentOut])
def list_payments(db: Session = Depends(get_db)):
    return [_out(p) for p in db.query(models.Payment).order_by(models.Payment.created_at.desc()).limit(50).all()]

@router.get("/{payment_id}", response_model=schemas.PaymentOut)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    p = db.query(models.Payment).filter_by(id=payment_id).first()
    if not p:
        raise HTTPException(404, "payment not found")
    return _out(p)

@router.get("/{payment_id}/events", response_model=list[schemas.EventOut])
def get_events(payment_id: str, db: Session = Depends(get_db)):
    evs = db.query(models.PaymentEvent).filter_by(payment_id=payment_id).order_by(models.PaymentEvent.created_at).all()
    return [{c.name: getattr(e, c.name) for c in e.__table__.columns} for e in evs]
