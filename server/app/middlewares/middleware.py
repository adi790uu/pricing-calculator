from functools import wraps
from http import HTTPStatus
from app.schemas.data_response_dto import ErrorResponse, GenericResponse
from fastapi import HTTPException
from loguru import logger

from app.core.exception import (
    DuplicateResourceCreateError,
    ResourceNotFoundError,
)


def router_exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as e:
            logger.error(f"HTTPException: {e.detail}")
            raise e
        except DuplicateResourceCreateError as e:
            logger.error(f"DuplicateResourceCreateError: {str(e)}")
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))
        except ResourceNotFoundError as e:
            logger.error(f"ResourceNotFoundError: {str(e)}")
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=str(e),
            )
        except ValueError as e:
            logger.exception(f"ValueError: {str(e)}")
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=str(e),
            )
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            response = GenericResponse(
                error=ErrorResponse(message="An unexpected error occurred")
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=response.model_dump(mode="json"),
            )

    return wrapper
