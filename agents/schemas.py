"""Structured decision output — mirrors contracts/decision_schema.json (P1 Day 3)."""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

ActionType = Literal["WAIT", "REPLACE", "ESCALATE"]

class EvidenceRef(BaseModel):
    tool: str
    summary: str
    ref_id: Optional[str] = None

class DuplicateRisk(BaseModel):
    is_duplicate_risk: bool = False
    matched_on: List[str] = Field(default_factory=list)
    existing_payment_id: Optional[str] = None

class DecisionOutput(BaseModel):
    incident_id: str
    action: ActionType
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning_summary: str = Field(min_length=10)
    evidence: List[EvidenceRef] = Field(default_factory=list)
    next_check_at: Optional[str] = None
    duplicate_risk: DuplicateRisk = Field(default_factory=DuplicateRisk)
    rule_version: str = "safety-v1"
