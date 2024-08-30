import io
from sys import exit as sys_exit

import paramiko
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from loguru import logger
from report_maker.config import config_obj


def receive_all_ips() -> list[str]:
    response = requests.get(
        f"http://{config_obj.CERT_PROVIDER_HOST}:{config_obj.CERT_PROVIDER_PORT}/all_ips"
    )

    json_data = response.json()
    if not json_data.get("all_ips"):
        logger.critical(
            f"{config_obj.CERT_PROVIDER_HOST}:{config_obj.CERT_PROVIDER_PORT}"
            " has provided unexpected response => {json_data}"
        )
        sys_exit(1)

    return json_data["all_ips"]


def get_private_key_by_ip(ip: str) -> bytes | None:
    response = requests.post(
        f"http://{config_obj.CERT_PROVIDER_HOST}:{config_obj.CERT_PROVIDER_PORT}/certs",
        json={
            "ip": ip
        }
    )

    json_data = response.json()
    if not json_data.get("private_key"):
        logger.critical(
            f"{config_obj.CERT_PROVIDER_HOST}:{config_obj.CERT_PROVIDER_PORT} "
            "has provided unexpected response => {json_data}"
        )
        return

    return json_data["private_key"]


def connect_to_server(host: str, private_key_str: str) -> paramiko.SSHClient:
    private_key_bytes = private_key_str.encode('utf-8')
    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None,
        backend=default_backend()
    )

    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,  # Convert to RSA PEM format
        encryption_algorithm=serialization.NoEncryption()
    )

    io_obj = io.StringIO(pem_private_key.decode('utf-8'))  # Convert to a file-like object

    private_key = paramiko.RSAKey.from_private_key(io_obj)

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh_client.connect(
        hostname=host,
        username=config_obj.VM_USER,
        pkey=private_key
    )

    return ssh_client


def execute_command(
    ssh_client: paramiko.SSHClient,
    host: str,
    command: str
) -> str:
    _, stdout, stderr = ssh_client.exec_command(command)
    stderr_data = stderr.read()
    if stderr_data:
        logger.error(
            f"Failed to run report generation script on {host} => {stderr_data}"
        )

    return stdout.read().decode()
