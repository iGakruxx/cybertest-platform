import json
import platform
import shutil
from dataclasses import dataclass
from ..core.process import run_command, ProcessResult

@dataclass
class LocalRecon:
    commands: list[ProcessResult]
    segments: list[str]
    warnings: list[str]

async def collect_local_reconnaissance() -> LocalRecon:
    """Sólo consulta el estado local; no emite paquetes hacia la red."""
    if platform.system().lower() == "linux" and shutil.which("ip"):
        commands = [
            await run_command(["ip", "-j", "address"], 15),
            await run_command(["ip", "-j", "route"], 15),
            await run_command(["ip", "-j", "neigh"], 15),
        ]
        segments = _connected_segments(commands[1].stdout)
        return LocalRecon(commands, segments, [])
    if platform.system().lower() == "windows":
        commands = [await run_command(["ipconfig", "/all"], 20), await run_command(["route", "print"], 20)]
        return LocalRecon(commands, [], ["Reconocimiento estructurado completo disponible en Kali Linux con iproute2."])
    return LocalRecon([], [], ["No se encontró iproute2; instale iproute2 en Kali Linux."])

def _connected_segments(route_json: str) -> list[str]:
    try:
        routes = json.loads(route_json)
    except json.JSONDecodeError:
        return []
    return sorted({route["dst"] for route in routes if route.get("type") == "unicast" and route.get("dst") and route.get("gateway") is None})
