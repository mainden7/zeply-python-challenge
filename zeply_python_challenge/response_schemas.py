from typing import Any

from pydantic import BaseModel
from starlette import status


class Message(BaseModel):
    """Define a response message."""

    msg: str


class ErrorResponseSchemas:
    """Define response schemas for error requests."""

    # === COMMON ERRORS ===
    BAD_REQUEST: dict[int | str, dict[str, Any]] = {
        status.HTTP_400_BAD_REQUEST: {
            "model": Message,
            "description": "(Bad Request) The request could not be performed",
        }
    }
    NOT_FOUND: dict[int | str, dict[str, Any]] = {
        status.HTTP_404_NOT_FOUND: {
            "model": Message,
            "description": "(Not Found) The requested resource was not found",
        },
    }
