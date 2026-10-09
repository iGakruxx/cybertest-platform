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

## 🚀 Instalación paso a paso

> Todo se ejecuta de forma local. Antes de iniciar un descubrimiento activo, registra y confirma por escrito el alcance autorizado. 🔐

### 🪟 Windows 10 / 11

1. Instala [Python 3.12 o superior](https://www.python.org/downloads/) y marca **Add Python to PATH** en el instalador.
2. Instala [Node.js LTS](https://nodejs.org/) para la interfaz. Si usarás el descubrimiento autorizado con Nmap, instala también [Nmap](https://nmap.org/download).
3. Abre PowerShell y entra en la carpeta del proyecto:

   ```powershell
   cd ruta\a\cybertest-platform
   ```

4. Crea y activa el entorno virtual:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Si PowerShell bloquea la activación, ejecuta una vez en esa terminal: `Set-ExecutionPolicy -Scope Process Bypass` y repite el comando de activación.

5. Instala el backend y sus herramientas de prueba:

   ```powershell
   python -m pip install --upgrade pip
   pip install -e '.[dev]'
   ```

6. En una primera terminal, inicia la API local:

   ```powershell
   uvicorn cybertest.main:app --host 127.0.0.1 --port 8765
   ```

   La API y su documentación quedan disponibles en `http://127.0.0.1:8765/docs`.

7. Abre una segunda terminal, activa de nuevo `.venv` si es necesario y levanta la interfaz:

   ```powershell
   cd ui
   npm install
   npm run dev
   ```

8. Abre `http://127.0.0.1:5173`. Vite redirige `/api` al backend local. ✅

### 🐉 Kali Linux / Debian / Ubuntu

1. Clona el repositorio y entra en su carpeta:

   ```bash
   git clone https://github.com/iGakruxx/cybertest-platform.git
   cd cybertest-platform
   ```

2. Instala los requisitos del sistema:

   ```bash
   sudo apt update
   sudo apt install -y python3 python3-venv python3-pip nodejs npm nmap
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

Para una guía ampliada, incluyendo solución de problemas y comprobaciones, consulta [docs/INSTALACION.md](docs/INSTALACION.md).

## 🧪 Verificación

```bash
pytest -q
cd ui
npm run build
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
