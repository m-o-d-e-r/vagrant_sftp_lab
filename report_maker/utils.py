from sys import exit as sys_exit

import requests
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
