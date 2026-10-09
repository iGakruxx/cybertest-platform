from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import Base, SessionLocal, engine
from .models import Asset, Audit, Evidence, Job, Scope
from .schemas import AuditCreate, JobCreate, ScopeCreate
from .core.policy import PolicyError, parse_authorized_private_network
from .reporting.export import export_assets_csv, export_html, export_json
from .scanners.dependencies import inventory_tools
from .services import jobs

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(title="CYBERTEST", version="0.1.0", lifespan=lifespan, docs_url="/docs")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def retrieve_audit(db: Session, audit_id: str) -> Audit:
    audit = db.get(Audit, audit_id)
    if not audit: raise HTTPException(404, "Auditoría no encontrada")
    return audit

@app.get("/health")
def health(): return {"status": "ok", "service": "CYBERTEST"}

@app.get("/tools")
def tools(): return inventory_tools()

@app.post("/audits", status_code=status.HTTP_201_CREATED)
def create_audit(payload: AuditCreate, db: Session = Depends(get_db)):
    audit = Audit(**payload.model_dump()); db.add(audit); db.commit(); db.refresh(audit); return audit

@app.get("/audits")
def list_audits(db: Session = Depends(get_db)):
    return db.scalars(select(Audit).order_by(Audit.created_at.desc())).all()

@app.post("/audits/{audit_id}/scopes", status_code=status.HTTP_201_CREATED)
def create_scope(audit_id: str, payload: ScopeCreate, db: Session = Depends(get_db)):
    retrieve_audit(db, audit_id)
    try: parse_authorized_private_network(payload.cidr)
    except PolicyError as exc: raise HTTPException(422, str(exc)) from exc
    scope = Scope(audit_id=audit_id, **payload.model_dump()); db.add(scope); db.commit(); db.refresh(scope); return scope

@app.get("/audits/{audit_id}/scopes")
def list_scopes(audit_id: str, db: Session = Depends(get_db)):
    retrieve_audit(db, audit_id); return db.scalars(select(Scope).where(Scope.audit_id == audit_id)).all()

@app.post("/audits/{audit_id}/jobs", status_code=status.HTTP_202_ACCEPTED)
def create_job(audit_id: str, payload: JobCreate, db: Session = Depends(get_db)):
    retrieve_audit(db, audit_id)
    params = payload.model_dump(exclude_none=True)
    if payload.kind == "nmap_discovery":
        if not payload.scope_id: raise HTTPException(422, "nmap_discovery requiere scope_id")
        scope = db.get(Scope, payload.scope_id)
        if not scope or scope.audit_id != audit_id: raise HTTPException(422, "Alcance inválido")
    job = Job(audit_id=audit_id, kind=payload.kind, parameters=params); db.add(job); db.commit(); db.refresh(job); jobs.start(job.id); return job

@app.get("/audits/{audit_id}/jobs")
def list_jobs(audit_id: str, db: Session = Depends(get_db)):
    retrieve_audit(db, audit_id); return db.scalars(select(Job).where(Job.audit_id == audit_id)).all()

@app.get("/audits/{audit_id}/assets")
def list_assets(audit_id: str, db: Session = Depends(get_db)):
    retrieve_audit(db, audit_id); return db.scalars(select(Asset).where(Asset.audit_id == audit_id)).all()

@app.get("/audits/{audit_id}/evidence")
def list_evidence(audit_id: str, db: Session = Depends(get_db)):
    retrieve_audit(db, audit_id); return db.scalars(select(Evidence).where(Evidence.audit_id == audit_id)).all()

@app.post("/jobs/{job_id}/cancel")
def cancel_job(job_id: str, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job: raise HTTPException(404, "Trabajo no encontrado")
    if not jobs.cancel(job_id): raise HTTPException(409, "El trabajo no está ejecutándose")
    return {"cancelled": True, "job_id": job_id}

@app.get("/audits/{audit_id}/report/{format}")
def report(audit_id: str, format: str, db: Session = Depends(get_db)):
    retrieve_audit(db, audit_id)
    if format == "json": return Response(export_json(db, audit_id), media_type="application/json")
    if format == "csv": return Response(export_assets_csv(db, audit_id), media_type="text/csv")
    if format == "html": return Response(export_html(db, audit_id), media_type="text/html")
    raise HTTPException(404, "Formato disponible: json, csv, html")
