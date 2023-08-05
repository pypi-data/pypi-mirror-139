import logging

from pydantic import BaseModel


class AppContext(BaseModel):
    env: str
    ipv4: str = ""
    ipv6: str = ""
    service_name: str
    service_version: str


class ActionContext(BaseModel):
    correlation_id: str = ""
    trace_id: str = ""
    root_action: str = ""
    current_action: str = ""
    user_id: str = ""


class LoggerService:
    def __init__(self, **kwargs):
        app_context = AppContext(**kwargs)
        self.environment = app_context.env
        context__dict_ = {
            **app_context.dict(),
            **ActionContext().dict()
        }

        self.logger = logging.LoggerAdapter(
            logging.getLogger(app_context.service_name),
            context__dict_
        )

    def info(self, message, *args, extra=None, **kwargs):
        request_context = ActionContext(**extra).dict() if extra else {}
        self.logger.extra = {
            **self.logger.extra,
            **request_context,
        }
        print(self.logger.extra)
        self.logger.info(message, *args, **kwargs)

    def debug(self, message, *args, extra=None, **kwargs):
        request_context = ActionContext(**extra).dict() if extra else {}
        self.logger.extra = {
            **self.logger.extra,
            **request_context,
        }
        self.logger.debug(message, *args, **kwargs)

    def warning(self, message, *args, extra=None, **kwargs):
        request_context = ActionContext(**extra).dict() if extra else {}
        self.logger.extra = {
            **self.logger.extra,
            **request_context,
        }
        self.logger.warning(message, *args, **kwargs)

    def error(self, message, *args, extra=None, **kwargs):
        request_context = ActionContext(**extra).dict() if extra else {}
        self.logger.extra = {
            **self.logger.extra,
            **request_context,
        }
        self.logger.error(message, *args, **kwargs)

    def exception(self, message, *args, extra=None, exc_info=True, **kwargs):
        request_context = ActionContext(**extra).dict() if extra else {}
        self.logger.extra = {
            **self.logger.extra,
            **request_context,
        }
        self.logger.exception(message, *args, exc_info=exc_info, **kwargs)

    def critical(self, message, *args, extra=None, **kwargs):
        request_context = ActionContext(**extra).dict() if extra else {}
        self.logger.extra = {
            **self.logger.extra,
            **request_context,
        }
        print(self.logger.extra)
        self.logger.critical(message, *args, **kwargs)
