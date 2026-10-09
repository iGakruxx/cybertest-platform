import asyncio
from datetime import datetime
from sqlalchemy import select
from .database import SessionLocal
from .evidence.store import save_text
from .models import Asset, Evidence, Job, Scope
from .network.local import collect_local_reconnaissance
from .scanners.nmap import discover
from .core.policy import permit_active_discovery

class JobService:
    def __init__(self):
        self.tasks: dict[str, asyncio.Task] = {}

    def start(self, job_id: str) -> None:
        self.tasks[job_id] = asyncio.create_task(self._execute(job_id))

    async def _execute(self, job_id: str) -> None:
        db = SessionLocal(); job = db.get(Job, job_id)
        try:
            job.status, job.started_at = "running", datetime.utcnow(); db.commit()
            if job.kind == "local_reconnaissance":
                recon = await collect_local_reconnaissance()
                body = "\n\n".join(f"$ {' '.join(c.argv)}\n{c.stdout}\n{c.stderr}" for c in recon.commands)
                body += "\nSegmentos conectados: " + ", ".join(recon.segments)
                path, digest = save_text(job.audit_id, "local-recon", body)
                db.add(Evidence(audit_id=job.audit_id, job_id=job.id, tool="local-system", command=[c.argv for c in recon.commands], path=path, sha256=digest))
            elif job.kind == "nmap_discovery":
                scope = db.get(Scope, job.parameters["scope_id"])
                if scope is None:
                    raise ValueError("El alcance fue eliminado antes de iniciar el trabajo")
                permit_active_discovery(scope, job.audit_id)
                result = await discover(scope.cidr, job.parameters.get("interface"))
                path, digest = save_text(job.audit_id, "nmap-discovery", result.stdout + "\n" + result.stderr)
                db.add(Evidence(audit_id=job.audit_id, job_id=job.id, tool="nmap", command=result.argv, path=path, sha256=digest))
                # Nmap XML will replace this conservative line parser in the enumeración phase.
                for line in result.stdout.splitlines():
                    if "Nmap scan report for " in line:
                        ip = line.rsplit(" ", 1)[-1].strip("()")
                        if not db.scalar(select(Asset).where(Asset.audit_id == job.audit_id, Asset.ip == ip)):
                            db.add(Asset(audit_id=job.audit_id, ip=ip, discovery_method="nmap_ping_scan", confidence="medium", source_segment=scope.cidr))
            job.status = "completed"
        except asyncio.CancelledError:
            job.status, job.error = "cancelled", "Cancelado por el operador"; raise
        except Exception as exc:
            job.status, job.error = "failed", str(exc)
        finally:
            job.finished_at = datetime.utcnow(); db.commit(); db.close(); self.tasks.pop(job_id, None)

    def cancel(self, job_id: str) -> bool:
        task = self.tasks.get(job_id)
        if not task: return False
        task.cancel(); return True

jobs = JobService()
