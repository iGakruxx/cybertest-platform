import asyncio
from dataclasses import dataclass

@dataclass
class ProcessResult:
    argv: list[str]
    stdout: str
    stderr: str
    returncode: int

async def run_command(argv: list[str], timeout: int = 30) -> ProcessResult:
    """Ejecuta una lista ya validada; nunca usa shell=True."""
    process = await asyncio.create_subprocess_exec(
        *argv, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
    except asyncio.CancelledError:
        process.terminate()
        await process.wait()
        raise
    except TimeoutError:
        process.terminate()
        await process.wait()
        raise RuntimeError(f"Tiempo máximo agotado: {' '.join(argv[:2])}")
    return ProcessResult(argv, stdout.decode(errors="replace"), stderr.decode(errors="replace"), process.returncode)
