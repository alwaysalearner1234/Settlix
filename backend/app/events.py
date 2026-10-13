"""Event bus — Redis Streams in docker, in-memory fallback for Phase 1 dev/tests."""
import os
import time
from typing import Dict, Any, List

MEMORY_BUS: List[Dict[str, Any]] = []

def publish_event(stream: str, data: Dict[str, Any]) -> str:
    url = os.getenv("REDIS_URL", "")
    try:
        if url:
            import redis
            r = redis.from_url(url, socket_connect_timeout=1)
            eid = r.xadd(stream, {k: str(v) for k, v in data.items()})
            return str(eid)
    except Exception:
        pass
    MEMORY_BUS.append({"stream": stream, "data": data, "ts": time.time()})
    return f"mem-{len(MEMORY_BUS)}"

def read_events() -> List[Dict[str, Any]]:
    return list(MEMORY_BUS)
