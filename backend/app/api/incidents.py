"""Incidents REST API (P2 Day 5) + detector helper (P1 Day 8 skeleton)."""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..events import publish_event

router = APIRouter(prefix="/incidents", tags=["incidents"])

def _out(i: models.Incident) -> dict:
    return {c.name: getattr(i, c.name) for c in i.__table__.columns}

@router.post("", response_model=schemas.IncidentOut)
def create_incident(body: schemas.IncidentIn, db: Session = Depends(get_db)):
    pay = db.query(models.Payment).filter_by(id=body.payment_id).first()
    if not pay:
        raise HTTPException(404, "payment not found")
    inc = models.Incident(payment_id=body.payment_id, type=body.type,
                          priority=body.priority, summary=body.summary or f"{body.type} for payment {body.payment_id[:8]}")
    db.add(inc)
    db.flush()  # generate inc.id before audit row
    db.add(models.AuditLog(incident_id=inc.id, actor="system", event="incident.created",
                           details={"payment_id": body.payment_id, "type": body.type}))
    db.commit(); db.refresh(inc)
    publish_event("incidents", {"incident_id": inc.id, "payment_id": body.payment_id})
    return _out(inc)

@router.get("", response_model=list[schemas.IncidentOut])
def list_incidents(db: Session = Depends(get_db)):
    return [_out(i) for i in db.query(models.Incident).order_by(models.Incident.created_at.desc()).limit(50).all()]

@router.get("/{incident_id}", response_model=schemas.IncidentOut)
def get_incident(incident_id: str, db: Session = Depends(get_db)):
    i = db.query(models.Incident).filter_by(id=incident_id).first()
    if not i:
        raise HTTPException(404, "incident not found")
    return _out(i)

def detect_overdue(db: Session) -> list[models.Incident]:
    """Phase 1 skeleton detector: any PENDING payment past due_at without an OPEN incident -> new incident."""
    now = datetime.utcnow()
    out = []
    for p in db.query(models.Payment).filter_by(status="PENDING").all():
        if p.due_at and p.due_at < now:
            exists = db.query(models.Incident).filter_by(payment_id=p.id, status="OPEN").first()
            if not exists:
                inc = models.Incident(payment_id=p.id, type="OVERDUE", priority="P2",
                                      summary=f"Payment {p.id[:8]} overdue (due {p.due_at})")
                db.add(inc); out.append(inc)
    if out:
        db.commit()
    return out
