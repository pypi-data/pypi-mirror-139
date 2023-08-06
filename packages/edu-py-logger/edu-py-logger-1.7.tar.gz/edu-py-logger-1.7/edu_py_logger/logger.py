import logging
import socket
from typing import Optional

from pydantic import BaseModel

from edu_py_logger.utils import get_ip_6


class AppContext(BaseModel):
    service_name: str
    service_version: str
    env: str
    ipv4: Optional[str] = ""
    ipv6: Optional[str] = ""


class ActionContext(BaseModel):
    correlation_id: Optional[str] = ""
    trace_id: Optional[str] = ""
    root_action: Optional[str] = ""
    current_action: Optional[str] = ""
    user_id: Optional[str] = ""
    transaction_id: Optional[str] = ""
    span_id: Optional[str] = ""
    duration: Optional[float]


class LoggerService:
    def __init__(self, service_name, service_version, env):
        app_context = AppContext(
            service_name=service_name,
            service_version=service_version,
            env=env,
            ipv4=socket.gethostbyname(socket.gethostname()),
            ipv6=get_ip_6(socket.gethostname()),
        )
        self.environment = app_context.env
        self.logger = logging.LoggerAdapter(
            logging.getLogger(app_context.service_name),
            {**app_context.dict(), **ActionContext().dict()},
        )

    def info(self, message, *args, extra=None, stage=None, **kwargs):
        self.prepare_context(extra, stage)
        self.logger.info(message, *args, **kwargs)

    def debug(self, message, *args, extra=None, stage=None, **kwargs):
        self.prepare_context(extra, stage)
        self.logger.debug(message, *args, **kwargs)

    def warning(self, message, *args, extra=None, stage=None, **kwargs):
        self.prepare_context(extra, stage)
        self.logger.warning(message, *args, **kwargs)

    def error(self, message, *args, extra=None, stage=None, **kwargs):
        self.prepare_context(extra, stage)
        self.logger.error(message, *args, **kwargs)

    def exception(
        self, message, *args, extra=None, stage=None, exc_info=True, **kwargs
    ):
        self.prepare_context(extra, stage)
        self.logger.exception(message, *args, exc_info=exc_info, **kwargs)

    def critical(self, message, *args, extra=None, stage=None, **kwargs):
        self.prepare_context(extra, stage)
        self.logger.critical(message, *args, **kwargs)

    def prepare_context(self, extra, stage):
        request_context = ActionContext(**extra).dict() if extra else {}
        self.logger.extra = {
            **self.logger.extra,
            **request_context,
            "stage": stage,
        }
