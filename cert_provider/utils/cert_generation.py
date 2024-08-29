from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

CERTS: dict[str, list[bytes, bytes]] = {}


def get_certs_by_ip(
    ip: str,
    as_strings: bool = True
) -> list[bytes, bytes] | list[str, str]:
    certs = CERTS.get(ip)
    if not certs:
        raise ValueError("Unexistent IP provided")

    if as_strings:
        return [cert.decode() for cert in certs]

    return certs


def generate_keys_pare() -> list[bytes, bytes]:
    key = rsa.generate_private_key(
        backend=default_backend(),
        public_exponent=65537,
        key_size=2048
    )

    private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    )

    public_key = key.public_key().public_bytes(
        serialization.Encoding.OpenSSH,
        serialization.PublicFormat.OpenSSH
    )

    return [private_key, public_key]


def generate_certs(ip_list: list[str]) -> None:
    for ip in ip_list:
        CERTS[ip] = generate_keys_pare()
