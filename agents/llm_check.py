"""LLM connection test (P1 Day 3). Passes with or without AWS creds — skips live call if missing."""
import os

def test_connection() -> dict:
    model = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
    region = os.getenv("AWS_REGION", "us-east-1")
    if not os.getenv("AWS_ACCESS_KEY_ID"):
        return {"ok": True, "mode": "mock", "note": f"No AWS creds; agent runs rule-based. Would use {model} in {region}."}
    try:
        import boto3
        boto3.client("bedrock-runtime", region_name=region).list_foundation_models()
        return {"ok": True, "mode": "live", "model": model}
    except Exception as e:
        return {"ok": False, "mode": "error", "error": str(e)[:300]}

if __name__ == "__main__":
    print(test_connection())
