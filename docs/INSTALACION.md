# 🚀 Instalación de CYBERTEST

Instalación local para desarrollo o laboratorio. Utiliza CYBERTEST sólo con autorización expresa y documentada. 🛡️

## Requisitos comunes

- 🐍 Python 3.11 o posterior.
- 🟢 Node.js 20 LTS o posterior con npm.
- 💾 Al menos 1 GB de espacio libre.
- 🔒 Acceso local a `127.0.0.1`; no expongas la API a Internet.

## Windows 11 o Windows 10

### 1. Instalar dependencias

Instala Python desde [python.org](https://www.python.org/downloads/windows/) y Node.js LTS desde [nodejs.org](https://nodejs.org/). Al instalar Python, activa **Add Python to PATH**.

```powershell
python --version
npm --version
```

### 2. Crear el entorno Python

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

Si PowerShell bloquea la activación:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar la interfaz

```powershell
Set-Location ui
npm install
npm run build
Set-Location ..
```

### 4. Ejecutar en desarrollo

Terminal 1:

```powershell
.\.venv\Scripts\python.exe -m uvicorn cybertest.main:app --host 127.0.0.1 --port 8765
```

Terminal 2:

```powershell
Set-Location ui
npm run dev
```

Visita `http://127.0.0.1:5173`. La API queda en `http://127.0.0.1:8765/docs`.

> ℹ️ Windows permite validar API e interfaz. Las integraciones basadas en `iproute2`, `arp-scan` y Nmap se ejecutan nativamente en Kali Linux.

## Kali Linux

### 1. Instalar paquetes

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nodejs npm iproute2 nmap
```

Opcionales según el alcance autorizado:

```bash
sudo apt install -y arp-scan tcpdump tshark dnsutils curl
```

No ejecutes toda la aplicación como `root`. Usa privilegios elevados sólo para una herramienta que los requiera y dentro del alcance autorizado. 🔐

### 2. Preparar CYBERTEST

```bash
git clone <URL-DEL-REPOSITORIO> cybertest
cd cybertest
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

### 3. Compilar la interfaz

```bash
cd ui
npm install
npm run build
cd ..
```

### 4. Iniciar el entorno

Terminal 1:

```bash
.venv/bin/uvicorn cybertest.main:app --host 127.0.0.1 --port 8765
```

Terminal 2:

```bash
cd ui && npm run dev
```

Abre `http://127.0.0.1:5173`, crea una auditoría con su referencia de autorización y registra un CIDR privado antes de realizar descubrimiento activo. 🎯

## 🧪 Comprobaciones posteriores

```bash
pytest -q
cd ui && npm run build
curl http://127.0.0.1:8765/health
```

La respuesta esperada es `{"status":"ok","service":"CYBERTEST"}`.

## 🧰 Solución de problemas

| Síntoma | Acción recomendada |
|---|---|
| `python` no se reconoce | Abre una terminal nueva y comprueba `PATH`. |
| `npm` no se reconoce | Reinstala Node.js LTS y abre una terminal nueva. |
| Puerto 8765 ocupado | Elige otro puerto y actualiza el proxy de Vite. |
| Nmap no aparece | Instálalo con `apt` y reinicia la API. |
| Alcance rechazado | Registra un CIDR privado explícito y su justificación. |

## 🔒 Recomendaciones para producción

- Mantén la API en `127.0.0.1` hasta incorporar autenticación y TLS.
- Usa PostgreSQL y migraciones para despliegues multiusuario.
- Protege `data/` con permisos del sistema operativo.
- Prueba sólo sobre laboratorios y activos incluidos en la autorización escrita.
