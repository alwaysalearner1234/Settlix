"""SQLAlchemy models — Phase 1 tables: suppliers, payments, events, incidents, decisions, actions, audit_logs."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, JSON, Integer
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

def new_id() -> str:
    return str(uuid.uuid4())

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(String, primary_key=True, default=new_id)
    name = Column(String, nullable=False)
    account_no = Column(String, nullable=False, default="ACC-000")
    risk_score = Column(Float, default=0.1)
    created_at = Column(DateTime, default=datetime.utcnow)

class Payment(Base):
    __tablename__ = "payments"
    id = Column(String, primary_key=True, default=new_id)
    supplier_id = Column(String, ForeignKey("suppliers.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    invoice_no = Column(String, nullable=False)
    po_no = Column(String, nullable=False, default="")
    status = Column(String, default="PENDING")  # INITIATED/PENDING/SETTLED/FAILED/RETURNED/UNKNOWN
    idempotency_key = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_at = Column(DateTime, default=datetime.utcnow)
    supplier = relationship("Supplier")

class PaymentEvent(Base):
    __tablename__ = "payment_events"
    id = Column(String, primary_key=True, default=new_id)
    payment_id = Column(String, ForeignKey("payments.id"), nullable=False)
    type = Column(String, nullable=False)  # CREATED/SENT/BANK_ACK/SETTLED/FAILED/RETURNED/TIMEOUT
    payload = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(String, primary_key=True, default=new_id)
    payment_id = Column(String, ForeignKey("payments.id"), nullable=False)
    type = Column(String, default="OVERDUE")  # OVERDUE/FAILED/UNKNOWN_STATUS/RETURNED/AMBIGUOUS
    status = Column(String, default="OPEN")  # OPEN/INVESTIGATING/WAITING/ESCALATED/RESOLVED/FAILED
    priority = Column(String, default="P2")
    summary = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

class Decision(Base):
    __tablename__ = "decisions"
    id = Column(String, primary_key=True, default=new_id)
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=False)
    action = Column(String, nullable=False)  # WAIT/REPLACE/ESCALATE
    confidence = Column(Float, nullable=False)
    reasoning_summary = Column(Text, default="")
    evidence_refs = Column(JSON, default=list)
    rule_version = Column(String, default="safety-v1")
    created_at = Column(DateTime, default=datetime.utcnow)

class Action(Base):
    __tablename__ = "actions"
    id = Column(String, primary_key=True, default=new_id)
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=False)
    decision_id = Column(String, ForeignKey("decisions.id"), nullable=True)
    kind = Column(String, nullable=False)  # RECHECK/SCHEDULE_RECHECK/CREATE_REPLACEMENT/ESCALATE_TO_HUMAN/NOOP
    payload = Column(JSON, default=dict)
    status = Column(String, default="PENDING")  # PENDING/DONE/BLOCKED/FAILED
    idempotency_key = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True, default=new_id)
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=True)
    actor = Column(String, nullable=False)  # agent/safety-engine/system/human/simulator
    event = Column(String, nullable=False)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
