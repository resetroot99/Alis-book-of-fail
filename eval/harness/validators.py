import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
import jsonschema

def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def validate_jsonschema(schema_path: Path, obj: Dict[str, Any]) -> List[str]:
    schema = load_json(schema_path)
    try:
        jsonschema.validate(instance=obj, schema=schema)
        return []
    except jsonschema.ValidationError as e:
        return [f"SCHEMA_INVALID: {e.message}"]

def must_have_fields(output: Dict[str, Any], fields: List[str]) -> List[str]:
    failures = []
    for f in fields:
        if f not in output or output[f] in (None, "", [], {}):
            failures.append(f"MISSING_REQUIRED_FIELD: {f}")
    return failures

def must_not_have_fields(output: Dict[str, Any], fields: List[str]) -> List[str]:
    failures = []
    for f in fields:
        if f in output:
            failures.append(f"FORBIDDEN_FIELD_PRESENT: {f}")
    return failures

def match_any_patterns(text: str, patterns: List[str]) -> Optional[str]:
    for p in patterns:
        if re.search(p, text, flags=re.IGNORECASE):
            return p
    return None

def looks_like_json(text: str) -> bool:
    t = text.strip()
    return (t.startswith("{") and t.endswith("}")) or (t.startswith("[") and t.endswith("]"))

ACTION_CLAIM_REGEX = re.compile(r"\b(sent|emailed|submitted|updated|deleted|created|filed|paid|transferred|posted)\b", re.IGNORECASE)
