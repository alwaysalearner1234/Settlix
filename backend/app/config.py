"""Backend config — env-driven, sqlite fallback for Phase 1 local dev."""
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./settlix.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
RULE_VERSION = "safety-v1"
CONFIDENCE_THRESHOLD = 0.80
