import shutil
import subprocess

TOOLS = ("ip", "nmap", "arp-scan", "tshark", "tcpdump", "dig", "curl")

def inventory_tools() -> list[dict]:
    result = []
    for name in TOOLS:
        path = shutil.which(name)
        version = None
        if path:
            try:
                output = subprocess.run([name, "--version"], capture_output=True, text=True, timeout=3, check=False)
                version = (output.stdout or output.stderr).splitlines()[0][:160]
            except (OSError, subprocess.TimeoutExpired):
                version = "instalada (versión no disponible)"
        result.append({"name": name, "installed": bool(path), "path": path, "version": version, "install": f"sudo apt install {name}"})
    return result
