"""Payment generator + seed data (P4 Day 2)."""
import random
import uuid

SUPPLIERS = [("Acme Components Ltd", "ACME-001"), ("Globex Parts", "GLXB-042"), ("Initech Supplies", "INIT-007")]

def generate(n: int = 5, seed: int = 42) -> list[dict]:
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        name, acc = rnd.choice(SUPPLIERS)
        out.append({
            "supplier_name": name, "account_no": acc,
            "amount": round(rnd.uniform(1000, 50000), 2),
            "invoice_no": f"INV-2026-{rnd.randint(100, 999)}",
            "po_no": f"PO-{rnd.randint(1000, 9999)}",
            "idempotency_key": f"gen-{uuid.uuid4().hex[:8]}",
        })
    return out

if __name__ == "__main__":
    import json
    print(json.dumps(generate(), indent=2))
