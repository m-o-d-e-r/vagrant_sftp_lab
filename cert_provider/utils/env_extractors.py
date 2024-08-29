import sys
from os import environ

from loguru import logger


def extract_servers_ip() -> list[str]:
    raw_server_list = environ.get("SFTP_SERVER_LIST", "")

    logger.info("SFTP_SERVER_LIST got from environments")

    server_list: list[str] = list(
        filter(
            lambda x: x,
            raw_server_list.split(" ")
        )
    )
    if not server_list:
        logger.error("variable SFTP_SERVER_LIST should be provided")
        sys.exit(0)

    logger.info(f"ssh keys should be generated for {server_list}")
    return server_list
