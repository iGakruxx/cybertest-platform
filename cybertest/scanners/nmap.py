from ..core.process import run_command, ProcessResult
from ..core.policy import parse_authorized_private_network

async def discover(cidr: str, interface: str | None = None) -> ProcessResult:
    network = parse_authorized_private_network(cidr)
    argv = ["nmap", "-sn", "-n", "--max-retries", "1", "--host-timeout", "10s", str(network)]
    if interface:
        argv.extend(["-e", interface])
    return await run_command(argv, timeout=180)
