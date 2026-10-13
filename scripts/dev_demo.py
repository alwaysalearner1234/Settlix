"""Phase 1 demo without docker: seed sqlite, run simulator scenario 3, investigate, print."""
import os, sys, json
os.environ.setdefault("DATABASE_URL", "sqlite:///./settlix.db")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.app.db import init_db
from simulator.run import run
from agents.investigator import investigate

if __name__ == "__main__":
    init_db()
    ids = run(3)  # hero: dangerous unknown
    d = investigate(ids["incident_id"], ids["payment_id"])
    print(json.dumps(d.model_dump(), indent=2))
    print("\nPhase 1 flow OK: payment -> incident -> agent decision (ESCALATE expected).")
