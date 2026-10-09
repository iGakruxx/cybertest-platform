# 🛡️ CYBERTEST

> Plataforma local, modular y orientada a evidencias para auditorías de redes **expresamente autorizadas**.

CYBERTEST organiza la evaluación desde el reconocimiento local hasta el informe técnico. El alcance, la autorización y la trazabilidad son requisitos de primer nivel. 🔐

## ✨ Estado actual

- 🗂️ Gestión persistente de auditorías y alcances autorizados.
- 🧭 Reconocimiento local pasivo de interfaces, rutas y vecinos.
- 🎯 Descubrimiento Nmap tipo `ping scan`, limitado a CIDR privados aprobados.
- ⚙️ Trabajos cancelables, con timeouts y sin ejecución arbitraria de shell.
- 🧾 Evidencias con hash SHA-256 e informes JSON, CSV y HTML.
- 🖥️ Interfaz React/Vite y API FastAPI con OpenAPI.

> ⛔ No incluye explotación automática, movimiento lateral ni persistencia. Úsalo sólo sobre activos incluidos explícitamente en una autorización escrita.

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

## 🚀 Instalación paso a paso

> Todo se ejecuta de forma local. Antes de iniciar un descubrimiento activo, registra y confirma por escrito el alcance autorizado. 🔐

### 🪟 Windows 10 / 11

1. Instala [Python 3.12 o superior](https://www.python.org/downloads/) y marca **Add Python to PATH** durante la instalación.
2. Instala [Node.js LTS](https://nodejs.org/). Para descubrimiento autorizado, instala también [Nmap](https://nmap.org/download).
3. Abre PowerShell y entra en la carpeta del proyecto:

   ```powershell
   cd ruta\a\cybertest-platform
   ```

4. Crea y activa el entorno virtual:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Si PowerShell bloquea la activación, ejecuta una vez `Set-ExecutionPolicy -Scope Process Bypass` y repite el último comando.

5. Instala el backend y las herramientas de prueba:

   ```powershell
   python -m pip install --upgrade pip
   pip install -e '.[dev]'
   ```

6. En una primera terminal, inicia la API local:

   ```powershell
   uvicorn cybertest.main:app --host 127.0.0.1 --port 8765
   ```

7. En una segunda terminal, inicia la interfaz:

   ```powershell
   cd ui
   npm install
   npm run dev
   ```

8. Abre `http://127.0.0.1:5173`. La documentación de la API está en `http://127.0.0.1:8765/docs`. ✅

### 🐉 Kali Linux / Debian / Ubuntu

1. Instala los requisitos del sistema:

   ```bash
   sudo apt update
   sudo apt install -y python3 python3-venv python3-pip nodejs npm nmap
   ```

2. Entra en la carpeta del proyecto:

   ```bash
   cd /ruta/a/cybertest-platform
   ```

3. Crea y activa el entorno virtual:

   ```bash
   python3 -m venv .venv
   . .venv/bin/activate
   ```

4. Instala el backend:

   ```bash
   python -m pip install --upgrade pip
   pip install -e '.[dev]'
   ```

5. En la primera terminal, inicia la API local:

   ```bash
   uvicorn cybertest.main:app --host 127.0.0.1 --port 8765
   ```

6. En otra terminal, inicia la interfaz:

   ```bash
   cd ui
   npm install
   npm run dev
   ```

7. Visita `http://127.0.0.1:5173`. La documentación de la API está en `http://127.0.0.1:8765/docs`. ✅

## 🧪 Verificación

```bash
pytest -q
cd ui
npm run build
```

## 📚 Documentación

- 🪟 [Instalación ampliada en Windows](docs/INSTALACION.md#windows-11-o-windows-10)
- 🐉 [Instalación ampliada en Kali Linux](docs/INSTALACION.md#kali-linux)
- 🧠 [Arquitectura y evolución](docs/architecture.md)
- 🔐 [Seguridad y autorización](docs/SEGURIDAD.md)
- 🤝 [Guía de contribución](CONTRIBUTING.md)

## 📄 Licencia

MIT. Consulta [LICENSE](LICENSE).

---

Hecho para auditorías responsables, repetibles y documentadas. 🛡️
