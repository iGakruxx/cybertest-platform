from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

def identifier() -> str:
    return str(uuid4())

class Audit(Base):
    __tablename__ = "audits"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=identifier)
    name: Mapped[str] = mapped_column(String(200))
    client: Mapped[str | None] = mapped_column(String(200), nullable=True)
    operator: Mapped[str] = mapped_column(String(200))
    mode: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(30), default="draft")
    authorization_ref: Mapped[str] = mapped_column(String(500))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Scope(Base):
    __tablename__ = "scopes"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=identifier)
    audit_id: Mapped[str] = mapped_column(ForeignKey("audits.id"), index=True)
    cidr: Mapped[str] = mapped_column(String(50))
    allow_active_discovery: Mapped[bool] = mapped_column(Boolean, default=False)
    allow_offensive_validation: Mapped[bool] = mapped_column(Boolean, default=False)
    exclusions: Mapped[list] = mapped_column(JSON, default=list)
    justification: Mapped[str] = mapped_column(Text)

class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=identifier)
    audit_id: Mapped[str] = mapped_column(ForeignKey("audits.id"), index=True)
    ip: Mapped[str] = mapped_column(String(45))
    mac: Mapped[str | None] = mapped_column(String(32), nullable=True)
    hostname: Mapped[str | None] = mapped_column(String(255), nullable=True)
    vendor: Mapped[str] = mapped_column(String(255), default="Desconocido")
    discovery_method: Mapped[str] = mapped_column(String(100))
    confidence: Mapped[str] = mapped_column(String(20), default="low")
    source_segment: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=identifier)
    audit_id: Mapped[str] = mapped_column(ForeignKey("audits.id"), index=True)
    kind: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(30), default="queued")
    parameters: Mapped[dict] = mapped_column(JSON, default=dict)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

class Evidence(Base):
    __tablename__ = "evidence"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=identifier)
    audit_id: Mapped[str] = mapped_column(ForeignKey("audits.id"), index=True)
    job_id: Mapped[str | None] = mapped_column(ForeignKey("jobs.id"), nullable=True)
    tool: Mapped[str] = mapped_column(String(100))
    command: Mapped[list] = mapped_column(JSON, default=list)
    path: Mapped[str] = mapped_column(String(500))
    sha256: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
