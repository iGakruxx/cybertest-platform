import csv
import json
from html import escape
from io import StringIO
from sqlalchemy import select
from ..models import Asset, Audit, Evidence, Job, Scope

def audit_snapshot(session, audit_id: str) -> dict:
    audit = session.get(Audit, audit_id)
    if not audit:
        raise LookupError("Auditoría inexistente")
    def records(cls): return [row.__dict__ | {} for row in session.scalars(select(cls).where(cls.audit_id == audit_id)).all()]
    def clean(row): return {k: v.isoformat() if hasattr(v, "isoformat") else v for k, v in row.items() if not k.startswith("_")}
    return {"audit": clean(audit.__dict__), "scope": [clean(x) for x in records(Scope)], "assets": [clean(x) for x in records(Asset)], "jobs": [clean(x) for x in records(Job)], "evidence": [clean(x) for x in records(Evidence)]}

def export_json(session, audit_id: str) -> str:
    return json.dumps(audit_snapshot(session, audit_id), ensure_ascii=False, indent=2)

def export_assets_csv(session, audit_id: str) -> str:
    assets = audit_snapshot(session, audit_id)["assets"]
    stream = StringIO()
    writer = csv.DictWriter(stream, fieldnames=["ip", "mac", "hostname", "vendor", "discovery_method", "confidence", "source_segment"])
    writer.writeheader(); writer.writerows([{key: asset.get(key) for key in writer.fieldnames} for asset in assets])
    return stream.getvalue()

def export_html(session, audit_id: str) -> str:
    snapshot = audit_snapshot(session, audit_id)
    assets = "".join(
        f"<tr><td>{escape(str(a['ip']))}</td><td>{escape(str(a.get('hostname') or ''))}</td>"
        f"<td>{escape(str(a['discovery_method']))}</td><td>{escape(str(a['confidence']))}</td></tr>"
        for a in snapshot["assets"]
    )
    name = escape(str(snapshot["audit"]["name"]))
    return f"<!doctype html><html lang=es><meta charset=utf-8><title>CYBERTEST</title><body><h1>Informe CYBERTEST</h1><p>Auditoría: {name}</p><h2>Activos</h2><table border=1><tr><th>IP</th><th>Nombre</th><th>Método</th><th>Confianza</th></tr>{assets}</table><p>Los resultados reflejan evidencia observada; no confirman explotación.</p></body></html>"
