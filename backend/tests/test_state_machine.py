"""State machine transition tests (P2 Day 3)."""
import pytest
from backend.app.state_machine import transition, IllegalTransition

def test_happy_path():
    assert transition("INITIATED", "PENDING") == "PENDING"
    assert transition("PENDING", "SETTLED") == "SETTLED"

def test_settled_terminal():
    with pytest.raises(IllegalTransition):
        transition("SETTLED", "PENDING")

def test_unknown_can_resolve():
    assert transition("UNKNOWN", "SETTLED") == "SETTLED"
    assert transition("UNKNOWN", "FAILED") == "FAILED"

def test_failed_only_retries_via_pending():
    assert transition("FAILED", "PENDING") == "PENDING"
    with pytest.raises(IllegalTransition):
        transition("FAILED", "SETTLED")
