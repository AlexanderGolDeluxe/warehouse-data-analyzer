from typing import Any

from fastapi import status
from pydantic import BaseModel


class DefaultAPIResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    data: Any = None
    error: str | None = None
    http_code: int = status.HTTP_200_OK


default_responses = {
    status.HTTP_200_OK: {
        "description": "Success",
        "content": {"application/json": {}}
    },
    status.HTTP_400_BAD_REQUEST: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": DefaultAPIResponse(
                    success=False,
                    message="BAD REQUEST",
                    http_code=status.HTTP_400_BAD_REQUEST
                ).model_dump()
            }
        }
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": DefaultAPIResponse(
                    success=False,
                    message="NOT FOUND",
                    http_code=status.HTTP_404_NOT_FOUND
                ).model_dump()
            }
        }
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "Unprocessable Entity",
        "content": {
            "application/json": {
                "example": DefaultAPIResponse(
                    success=False,
                    message="UNPROCESSABLE ENTITY",
                    data={
                        "detail": [{
                            "loc": ["string", 0],
                            "msg": "string",
                            "type": "string"
                        }]
                    },
                    http_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                ).model_dump()
            }
        }
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": DefaultAPIResponse(
                    success=False,
                    message="INTERNAL SERVER ERROR",
                    http_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                ).model_dump()
            }
        }
    }
}
