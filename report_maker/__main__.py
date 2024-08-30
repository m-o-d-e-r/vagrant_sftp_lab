from os import environ
from sys import exit as sys_exit

import requests
from dotenv import load_dotenv
from loguru import logger
from report_maker.utils import receive_all_ips

load_dotenv()


def get_required_env_var(env_var_name: str) -> str:
    env_var_value = environ.get(env_var_name)
    if not env_var_value:
        logger.critical(f"environment variable {env_var_name} was not provided")
        sys_exit(1)

    return env_var_value


CERT_PROVIDER_HOST = get_required_env_var("CERT_PROVIDER_HOST")
CERT_PROVIDER_PORT = get_required_env_var("CERT_PROVIDER_PORT")


print(receive_all_ips(CERT_PROVIDER_HOST, CERT_PROVIDER_PORT))
