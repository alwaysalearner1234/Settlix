# Settlix — Phase 1 Foundation ✅

AI payment investigator + money-safety layer. A payment appears failed but the original
status is ambiguous → Settlix investigates, blocks a dangerous duplicate, and escalates
for human review when evidence is insufficient.

## Phase 1 acceptance (Day 7)
One simulated payment → incident row → agent output → shown in UI.

```bash
docker compose up -d postgres redis
pip install -r backend/requirements.txt -r agents/requirements.txt -r simulator/requirements.txt
python -m backend.app.seed            # creates supplier + overdue payment + incident
python scripts/dev_demo.py            # scenario 3 -> ESCALATE 54%
pytest -q                             # state machine + API + end-to-end
cd frontend && npm install && npm run dev
```

## Layout
- `contracts/` — locked Day-1 API contracts (decision JSON, incident schema, 10 tool signatures)
- `backend/` — FastAPI + SQLAlchemy (Postgres, sqlite fallback), state machine, REST, Redis Streams bus
- `agents/` — investigator loop, 10 tools (mock now, real via `SETTLIX_API`), prompts, evidence, Pydantic output
- `simulator/` — payment generator, bank behaviours, event generator, 5 scenarios, `run.py`
- `frontend/` — React+TS+Tailwind: Overview, IncidentCard, KPI cards, Detail shell
- `tests/test_phase1_integration.py` — full flow test

## Team
P1 lidiya (AI), P2 kishoreram (safety), P3 kumar (frontend), P4 vikram/lidiya (sim/infra/QA/demo).

## Next (Phase 2)
Detector + Safety Engine (WAIT/REPLACE/ESCALATE), Duplicate Guard, idempotency, WebSocket live UI.
