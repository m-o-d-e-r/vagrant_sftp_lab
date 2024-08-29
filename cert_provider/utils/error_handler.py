from flask import json, make_response
from loguru import logger
from werkzeug.exceptions import HTTPException


def handle_error(e: HTTPException | Exception):
    logger.error(e)

    is_common_exception = False
    if not issubclass(e.__class__, HTTPException):
        is_common_exception = True

    response = e.get_response() if not is_common_exception else make_response()
    response.data = json.dumps({
        "code": e.code if not is_common_exception else 400,
        "description": e.description if not is_common_exception else str(e),
    })
    response.content_type = "application/json"
    return response
