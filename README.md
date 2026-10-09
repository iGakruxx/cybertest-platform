# 🛡️ CYBERTEST

> Plataforma local, modular y orientada a evidencias para auditorías de redes **expresamente autorizadas**.

CYBERTEST ayuda a organizar el ciclo de evaluación desde el reconocimiento local hasta el informe técnico, sin convertirse en un lanzador de comandos sin control. La plataforma trata el alcance, la autorización y la trazabilidad como requisitos de primer nivel. 🔐

## ✨ Estado actual

La versión inicial incluye una base funcional para operar y evolucionar de forma segura:

- 🗂️ Gestión persistente de auditorías y alcances autorizados.
- 🧭 Reconocimiento local pasivo de interfaces, rutas y vecinos.
- 🎯 Descubrimiento Nmap de tipo `ping scan`, limitado a CIDR privados aprobados.
- ⚙️ Trabajos asíncronos cancelables, con timeouts y sin invocación de shell.
- 🧾 Evidencias redactadas con hash SHA-256 e informes JSON, CSV y HTML.
- 🖥️ Interfaz React/Vite de inicio y API FastAPI documentada con OpenAPI.
- ✅ Pruebas de política de alcance y verificación de compilación.

La correlación de CVE, enumeración avanzada, PDF, autenticación local y validación ofensiva aislada forman parte de las siguientes fases. No se presentan como funcionalidades terminadas.

## 🚦 Principios de uso seguro

- ✅ Opera únicamente sobre activos y segmentos autorizados por escrito.
- ✅ El descubrimiento activo exige un CIDR privado explícito y el permiso correspondiente.
- ✅ Las evidencias almacenan los comandos estructurados y su resultado, no secretos innecesarios.
- ⛔ No hay ejecución de shell arbitraria, movimiento lateral, persistencia ni explotación automática.
- ⛔ La validación ofensiva queda deshabilitada en esta entrega inicial.

## 🏗️ Arquitectura

```text
🖥️ React + TypeScript → 🔌 FastAPI local (127.0.0.1)
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
             🧠 Core       🗃️ SQLite    ⚙️ Adaptadores
                              │
                              ▼
                    🧾 Evidencias SHA-256 → 📊 Informes
```

Consulta la [arquitectura detallada](docs/architecture.md), el [modelo de seguridad](docs/SEGURIDAD.md) y la [guía de instalación](docs/INSTALACION.md).

## 🚀 Inicio rápido

```bash
python -m venv .venv
# Linux/macOS: . .venv/bin/activate
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -e '.[dev]'
uvicorn cybertest.main:app --host 127.0.0.1 --port 8765
```

La documentación interactiva queda en `http://127.0.0.1:8765/docs`.

Para la interfaz:

```bash
cd ui
npm install
npm run dev
```

Abre `http://127.0.0.1:5173`; Vite redirige `/api` al backend local.

## 🧪 Verificación

```bash
pytest -q
cd ui && npm run build
```

## 📚 Documentación

- 🪟 [Instalación en Windows](docs/INSTALACION.md#windows-11-o-windows-10)
- 🐉 [Instalación en Kali Linux](docs/INSTALACION.md#kali-linux)
- 🧠 [Arquitectura y evolución](docs/architecture.md)
- 🔐 [Seguridad y autorización](docs/SEGURIDAD.md)
- 🤝 [Guía de contribución](CONTRIBUTING.md)

## 📄 Licencia

MIT. Consulta [LICENSE](LICENSE).

---

Hecho para auditorías responsables, repetibles y documentadas. 🛡️
