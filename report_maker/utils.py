from sys import exit as sys_exit

import requests
from loguru import logger


def receive_all_ips(host: str, port: str | int) -> list[str]:
    response = requests.get(f"http://{host}:{port}/all_ips")

    json_data = response.json()
    if not json_data.get("all_ips"):
        logger.critical(
            f"{host}:{port} has provided unexpected response => {json_data}"
        )
        sys_exit(1)

    return json_data["all_ips"]
