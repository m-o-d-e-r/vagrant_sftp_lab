
from flask import request
from werkzeug.exceptions import BadRequest


def get_json() -> dict:
    try:
        json_data = request.get_json(force=True)
        if not isinstance(json_data, dict):
            return {}
        return json_data
    except Exception as exc:
        raise BadRequest(
            description="Invalid JSON data provided"
        ) from exc
