"""Políticas de alcance: el descubrimiento activo nunca se infiere de rutas."""
from ipaddress import ip_network, IPv4Network, IPv6Network

class PolicyError(ValueError):
    pass

def parse_authorized_private_network(cidr: str) -> IPv4Network | IPv6Network:
    try:
        network = ip_network(cidr, strict=False)
    except ValueError as exc:
        raise PolicyError("El alcance debe ser un CIDR válido") from exc
    if not network.is_private:
        raise PolicyError("Sólo se permiten redes privadas explícitamente autorizadas")
    return network

def permit_active_discovery(scope, audit_id: str) -> None:
    if scope.audit_id != audit_id:
        raise PolicyError("El alcance no pertenece a esta auditoría")
    parse_authorized_private_network(scope.cidr)
    if not scope.allow_active_discovery:
        raise PolicyError("El alcance no autoriza descubrimiento activo")

def permit_offensive_validation(scope, audit_id: str) -> None:
    permit_active_discovery(scope, audit_id)
    if not scope.allow_offensive_validation:
        raise PolicyError("La validación ofensiva requiere autorización específica")
