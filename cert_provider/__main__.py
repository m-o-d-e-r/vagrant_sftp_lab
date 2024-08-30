from os import environ

from cert_provider.models.keys_models import KeysByIPModel
from cert_provider.utils.cert_generation import CERTS, generate_certs, get_certs_by_ip
from cert_provider.utils.env_extractors import extract_servers_ip
from cert_provider.utils.error_handler import handle_error
from cert_provider.utils.requests import get_json
from dotenv import load_dotenv
from flask import Flask, jsonify
from loguru import logger
from werkzeug.exceptions import BadRequest

load_dotenv()

generate_certs(extract_servers_ip())

app = Flask(__name__)

app.register_error_handler(Exception, handle_error)


@app.post("/certs")
def get_cert():
    try:
        user_json = KeysByIPModel(**get_json())
    except Exception as exc:
        logger.error(exc)
        raise BadRequest(
            description=str(exc)
        ) from exc

    certs = get_certs_by_ip(user_json.ip)

    return jsonify(
        {
            "private_key": certs[0],
            "public_key": certs[1]
        }
    )


@app.get("/all_ips")
def get_all_ips():
    return jsonify(
        {
            "all_ips": list(CERTS.keys())
        }
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=bool(environ.get("DEBUG_MODE", ""))
    )
