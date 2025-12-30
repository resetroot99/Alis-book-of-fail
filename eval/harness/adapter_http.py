import requests
from typing import Any, Dict

class HttpAdapter:
    def __init__(self, base_url: str, timeout_s: int = 60):
        if not base_url:
            raise ValueError("base_url is required for HTTP adapter.")
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s

    def run_case(self, case: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "case_id": case["id"],
            "inputs": case.get("inputs", {}),
            "context": case.get("context", {}),
            "fixtures": case.get("fixtures", {}),
            "options": {"trace": True, "deterministic": True},
        }
        r = requests.post(f"{self.base_url}/eval/run", json=payload, timeout=self.timeout_s)
        r.raise_for_status()
        data = r.json() if r.content else {}

        return {
            "outputs": data.get("outputs", {}),
            "policy": data.get("policy", {"refuse": False, "abstain": False, "escalate": False, "reasons": []}),
            "retrieval": data.get("retrieval", {"queries": [], "doc_ids": []}),
            "actions": data.get("actions", []),
            "steps": data.get("steps", []),
            "metrics": data.get("metrics", {}),
        }
