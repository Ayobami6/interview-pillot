from functools import wraps
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from api.schemas.service_response import (
    InternalServerException,
    ServiceResponse,
    ServiceException,
    ServiceErrorResponse,
)

async def exception_handler(
    request: Request, exc: ServiceException
) -> ServiceErrorResponse:
    """FastAPI exception handler for ServiceException."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ServiceErrorResponse(
            success=False,
            message=exc.message,
            status_code=exc.status_code,
            data=None,
            traceback=getattr(exc, 'traceback', None),
        ).model_dump(exclude_none=True),
    )

def exception_before_advice(func):
    """Decorator to catch exceptions and raise ServiceException."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, ServiceException):
                raise e
            elif isinstance(e, HTTPException):
                raise ServiceException(
                    status_code=e.status_code,
                    message=e.detail,
                )
            else:
                # Log the actual error here
                print(f"Unhandled error: {e}")
                raise InternalServerException()

    return wrapper
