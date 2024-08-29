from cert_provider.utils.cert_generation import generate_certs, get_certs_by_ip
from cert_provider.utils.env_extractors import extract_servers_ip
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from loguru import logger

load_dotenv()  # take environment variables from .env.

generate_certs(extract_servers_ip())

app = Flask(__name__)


@app.post("/certs")
def get_cert():
    # NOTE: this code will be refactored, i promise)
    # It's just for test purposes

    try:
        user_json = request.get_json(force=True)
    except Exception as exc:
        logger.error(exc)
        return jsonify(
            {
                "error": "invalid JSON provided"
            }
        )

    if not user_json.get("ip"):
        return jsonify(
            {
                "error": "'ip' field was not provided"
            }
        )

    try:
        certs = get_certs_by_ip(user_json["ip"])
    except Exception as exc:
        logger.error(exc)
        return jsonify(
            {
                "error": str(exc)
            }
        )

    return jsonify(
        {
            "private_key": certs[0],
            "public_key": certs[1]
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
