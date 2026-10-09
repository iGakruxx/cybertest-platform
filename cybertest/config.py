from pathlib import Path
import os

DATA_DIR = Path(os.getenv("CYBERTEST_DATA_DIR", "data"))
DATABASE_URL = os.getenv("CYBERTEST_DATABASE_URL", f"sqlite:///{DATA_DIR / 'cybertest.db'}")
EVIDENCE_DIR = Path(os.getenv("CYBERTEST_EVIDENCE_DIR", str(DATA_DIR / "evidence")))
MAX_CONCURRENT_JOBS = int(os.getenv("CYBERTEST_MAX_CONCURRENT_JOBS", "2"))
LOCAL_BIND_HOST = os.getenv("CYBERTEST_HOST", "127.0.0.1")
