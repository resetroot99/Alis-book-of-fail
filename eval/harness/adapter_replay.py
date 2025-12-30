import json
from pathlib import Path
from typing import Any, Dict

class ReplayAdapter:
    def __init__(self, replay_dir: Path):
        self.replay_dir = replay_dir

    def run_case(self, case: Dict[str, Any]) -> Dict[str, Any]:
        p = self.replay_dir / f"{case['id']}.json"
        if not p.exists():
            return {
                "outputs": {"final_text": "REPLAY_STUB", "decision": "PASS"},
                "policy": {"refuse": False, "abstain": False, "escalate": False, "reasons": ["replay_stub"]},
                "retrieval": {"queries": [], "doc_ids": []},
                "actions": [],
                "steps": [],
                "metrics": {"latency_ms": 0}
            }
        return json.loads(p.read_text(encoding="utf-8"))
