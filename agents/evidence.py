"""Evidence aggregator skeleton (P1 Day 4)."""
from typing import Dict, Any, List

def aggregate(calls: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Merge tool outputs keyed by tool name; keeps raw blobs for audit."""
    evidence: Dict[str, Any] = {}
    for c in calls:
        tool = c.get("tool", "unknown")
        evidence[tool] = c
    return evidence

def summarize(evidence: Dict[str, Any]) -> str:
    parts = []
    for tool, blob in evidence.items():
        parts.append(f"{tool}: {str(blob)[:160]}")
    return " | ".join(parts)
