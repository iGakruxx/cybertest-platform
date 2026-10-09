from datetime import datetime
from hashlib import sha256
from pathlib import Path
from uuid import uuid4
from ..config import EVIDENCE_DIR

REDACTED_MARKERS = ("password=", "token=", "authorization: bearer ")

def redact(text: str) -> str:
    lines = []
    for line in text.splitlines():
        lowered = line.lower()
        lines.append("[REDACTED: possible secret]" if any(x in lowered for x in REDACTED_MARKERS) else line)
    return "\n".join(lines)

def save_text(audit_id: str, name: str, content: str) -> tuple[str, str]:
    safe_name = "".join(c for c in name if c.isalnum() or c in "._-")[:80] or "evidence"
    directory = EVIDENCE_DIR / audit_id
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{datetime.utcnow():%Y%m%dT%H%M%SZ}_{uuid4().hex[:8]}_{safe_name}.txt"
    cleaned = redact(content)
    path.write_text(cleaned, encoding="utf-8")
    return str(path), sha256(cleaned.encode()).hexdigest()
