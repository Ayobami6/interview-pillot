from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
import traceback
import logging

logger = logging.getLogger(__name__)

# Mocking configs for now, will add a proper config file later
DEBUG = True 

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class ServiceResponse(BaseSchema):
    message: str
    success: bool
    status_code: int
    data: Optional[Any] = None

class ServiceErrorResponse(BaseSchema):
    message: str
    success: bool
    status_code: int
    traceback: Optional[str] = None

class ServiceException(Exception):
    def __init__(self, **kwargs):
        self.status_code = kwargs.get("status_code", 500)
        self.message = kwargs.get("message", "An error occurred")
        self.traceback = None
        self.success: bool = False
        self._log_exception()

    def _log_exception(self):
        if self.traceback:
            logger.error(self.traceback)
        if DEBUG:
            traceback.print_exc()

class InternalServerException(ServiceException):
    def __init__(self) -> None:
        super().__init__(status_code=500, message="Don't panic, this is from us!")
        if DEBUG:
            self.traceback = traceback.format_exc()
        else:
            self.traceback = None
