"""FastAPI entrypoint — wires routers, inits DB, exposes /health."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db
from .api import payments, suppliers, incidents

app = FastAPI(title="Settlix API", version="0.1.0-phase1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(payments.router)
app.include_router(suppliers.router)
app.include_router(incidents.router)

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok", "service": "settlix-backend", "phase": 1}
