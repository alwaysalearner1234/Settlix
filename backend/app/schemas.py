"""Pydantic request/response schemas (mirrors contracts/incident_schema.json)."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class SupplierIn(BaseModel):
    name: str
    account_no: str = "ACC-000"
    risk_score: float = 0.1

class SupplierOut(SupplierIn):
    id: str
    created_at: datetime

class PaymentIn(BaseModel):
    supplier_id: str
    amount: float
    currency: str = "USD"
    invoice_no: str
    po_no: str = ""
    idempotency_key: str
    due_hours: int = 48

class PaymentOut(BaseModel):
    id: str
    supplier_id: str
    amount: float
    currency: str
    invoice_no: str
    po_no: str
    status: str
    idempotency_key: str
    created_at: datetime
    due_at: datetime

class EventOut(BaseModel):
    id: str
    payment_id: str
    type: str
    payload: Dict[str, Any] = {}
    created_at: datetime

class IncidentIn(BaseModel):
    payment_id: str
    type: str = "OVERDUE"
    priority: str = "P2"
    summary: str = ""

class IncidentOut(BaseModel):
    id: str
    payment_id: str
    type: str
    status: str
    priority: str
    summary: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
