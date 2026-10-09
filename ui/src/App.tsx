import { FormEvent, useEffect, useState } from "react";

type Audit = { id: string; name: string; client?: string; operator: string; mode: string; status: string; created_at: string };
type Tool = { name: string; installed: boolean; version?: string };
const api = (path: string, options?: RequestInit) => fetch(`/api${path}`, { headers: { "Content-Type": "application/json" }, ...options });

export default function App() {
  const [audits, setAudits] = useState<Audit[]>([]);
  const [tools, setTools] = useState<Tool[]>([]);
  const [notice, setNotice] = useState("Cargando estado local…");
  const refresh = async () => {
    try {
      const [auditResponse, toolResponse] = await Promise.all([api("/audits"), api("/tools")]);
      setAudits(await auditResponse.json()); setTools(await toolResponse.json()); setNotice("API local conectada.");
    } catch { setNotice("La API local no está disponible. Inicie uvicorn en 127.0.0.1:8765."); }
  };
  useEffect(() => { void refresh(); }, []);
  const createAudit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); const form = new FormData(event.currentTarget);
    const response = await api("/audits", { method: "POST", body: JSON.stringify({ name: form.get("name"), client: form.get("client") || null, operator: form.get("operator"), mode: form.get("mode"), authorization_ref: form.get("authorization") }) });
    setNotice(response.ok ? "Auditoría creada. Añada un alcance explícito antes de cualquier prueba activa." : "No se pudo crear la auditoría.");
    if (response.ok) { event.currentTarget.reset(); await refresh(); }
  };
  return <main>
    <aside><div className="brand"><span>◈</span> CYBERTEST</div><nav><a className="active">Dashboard</a><a>Nueva auditoría</a><a>Inventario</a><a>Vulnerabilidades</a><a>Evidencias</a><a>Informes</a><a>Herramientas</a></nav><small>Operación local · alcance obligatorio</small></aside>
    <section className="content"><header><div><p className="eyebrow">PLATAFORMA DE AUDITORÍA</p><h1>Centro de operaciones</h1><p>{notice}</p></div><button onClick={() => void refresh()}>Actualizar</button></header>
      <div className="metrics"><Metric label="Auditorías" value={audits.length} /><Metric label="Herramientas listas" value={tools.filter(t => t.installed).length} /><Metric label="Activos" value="—" /><Metric label="Hallazgos confirmados" value="—" /></div>
      <div className="columns"><article><h2>Nueva auditoría</h2><form onSubmit={createAudit}><label>Proyecto<input required name="name" minLength={3} placeholder="Red de laboratorio" /></label><label>Cliente / entorno<input name="client" placeholder="Laboratorio autorizado" /></label><label>Operador<input required name="operator" placeholder="Nombre del auditor" /></label><label>Modo<select name="mode"><option value="black_box">Caja negra</option><option value="grey_box">Caja gris</option><option value="white_box">Caja blanca</option></select></label><label>Referencia de autorización<input required name="authorization" placeholder="Ticket, contrato o ID de aprobación" /></label><button type="submit">Crear auditoría</button></form></article>
      <article><h2>Auditorías recientes</h2>{audits.length ? <table><thead><tr><th>Proyecto</th><th>Modo</th><th>Estado</th></tr></thead><tbody>{audits.map(a => <tr key={a.id}><td>{a.name}<small>{a.operator}</small></td><td>{a.mode.replace("_", " ")}</td><td><span className="status">{a.status}</span></td></tr>)}</tbody></table> : <p className="empty">Aún no hay auditorías. Las pruebas activas no se habilitan sin alcance documentado.</p>}</article></div>
      <article><h2>Dependencias del sistema</h2><div className="tools">{tools.map(t => <div key={t.name} className={t.installed ? "tool ready" : "tool"}><b>{t.name}</b><span>{t.installed ? t.version || "Instalada" : "No instalada"}</span></div>)}</div></article>
    </section>
  </main>;
}
function Metric({ label, value }: { label: string; value: string | number }) { return <div className="metric"><span>{label}</span><strong>{value}</strong></div>; }
