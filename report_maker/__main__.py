import json
from os import environ
from pathlib import Path
from sys import exit as sys_exit

from dotenv import load_dotenv
from flask import Flask, render_template
from loguru import logger
from report_maker.config import config_obj
from report_maker.utils import (
    connect_to_server,
    execute_command,
    receive_all_ips,
    receive_all_privates_keys,
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
SERVERS_PRIVATE_KEYS: dict[str, str] = receive_all_privates_keys(SERVERS_TO_VISIT)


app = Flask(__file__, template_folder=Path(__file__).parent / "templates")


@app.get("/")
def receive_report():
    raw_reports_dict: dict[str, dict] = {}
    for server_ip, private_key in SERVERS_PRIVATE_KEYS.items():
        ssh_client = connect_to_server(server_ip, private_key)

        execute_command(ssh_client, server_ip, "bash generate_raw_report.sh")
        raw_report = execute_command(
            ssh_client,
            server_ip,
            "cat raw_report.json"
        )

        logger.info(f"Received raw report from {server_ip} => {raw_report}")

        raw_reports_dict[server_ip] = json.loads(raw_report)

    return render_template(
        "index.html",
        report_data=raw_reports_dict
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
