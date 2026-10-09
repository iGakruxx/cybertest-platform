import pytest
from cybertest.core.policy import PolicyError, parse_authorized_private_network

@pytest.mark.parametrize("cidr", ["10.1.0.0/16", "192.168.5.0/24", "fd00::/64"])
def test_private_cidrs_allowed(cidr):
    assert parse_authorized_private_network(cidr)

@pytest.mark.parametrize("cidr", ["8.8.8.0/24", "1.1.1.1/32", "not-a-network"])
def test_public_or_invalid_cidrs_are_rejected(cidr):
    with pytest.raises(PolicyError):
        parse_authorized_private_network(cidr)
