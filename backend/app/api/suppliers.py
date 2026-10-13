"""Suppliers REST API."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

@router.post("", response_model=schemas.SupplierOut)
def create_supplier(body: schemas.SupplierIn, db: Session = Depends(get_db)):
    s = models.Supplier(name=body.name, account_no=body.account_no, risk_score=body.risk_score)
    db.add(s); db.commit(); db.refresh(s)
    return {c.name: getattr(s, c.name) for c in s.__table__.columns}

@router.get("", response_model=list[schemas.SupplierOut])
def list_suppliers(db: Session = Depends(get_db)):
    return [{c.name: getattr(s, c.name) for c in s.__table__.columns}
            for s in db.query(models.Supplier).limit(50).all()]

@router.get("/{supplier_id}", response_model=schemas.SupplierOut)
def get_supplier(supplier_id: str, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    s = db.query(models.Supplier).filter_by(id=supplier_id).first()
    if not s:
        raise HTTPException(404, "supplier not found")
    return {c.name: getattr(s, c.name) for c in s.__table__.columns}
