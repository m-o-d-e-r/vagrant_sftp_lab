from os import environ
from sys import exit as sys_exit

from dotenv import load_dotenv
from loguru import logger
from report_maker.config import config_obj
from report_maker.utils import (
    connect_to_server,
    execute_command,
    get_private_key_by_ip,
    receive_all_ips,
)

load_dotenv()


def get_required_env_var(env_var_name: str) -> str:
    env_var_value = environ.get(env_var_name)
    if not env_var_value:
        logger.critical(f"environment variable {env_var_name} was not provided")
        sys_exit(1)

    return env_var_value


config_obj.CERT_PROVIDER_HOST = get_required_env_var("CERT_PROVIDER_HOST")
config_obj.CERT_PROVIDER_PORT = get_required_env_var("CERT_PROVIDER_PORT")

SERVERS_TO_VISIT: list[str] = receive_all_ips()

private_keys_dict: dict[str, str] = {}
for server_ip in SERVERS_TO_VISIT:
    private_key = get_private_key_by_ip(server_ip)

    if not private_key:
        logger.warning(f"Failed to receive private key for {server_ip}")
        continue

    private_keys_dict[server_ip] = private_key


for server_ip, private_key in private_keys_dict.items():
    ssh_client = connect_to_server(server_ip, private_key)

    execute_command(ssh_client, server_ip, "bash generate_raw_report.sh")
    raw_report = execute_command(ssh_client, server_ip, "cat raw_report.json")

    logger.info(f"Received raw report from {server_ip} => {raw_report}")
