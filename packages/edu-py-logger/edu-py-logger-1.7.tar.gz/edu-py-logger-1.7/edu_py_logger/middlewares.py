import datetime
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware


class TraceIdProcessTimeMiddleware(BaseHTTPMiddleware):
    def __init__(self, *args, logger=None, **kwargs) -> None:
        self.logger = logger
        super().__init__(*args, **kwargs)

    async def dispatch(self, request, call_next):
        start_time = datetime.datetime.now()
        request.state.trace_id = str(uuid4())
        request.state.time_started = start_time
        extra = {
            "correlation_id": request.headers.get("x-correlation-id"),
            "root_action": request.headers.get("x-root-action"),
            "user_id": request.headers.get("x-user-id"),
            "transaction_id": request.headers.get("x-transaction-id"),
            "span_id": request.headers.get("x-span-id"),
            "current_action": f"{request.method} {str(request.url.path)}",
            "trace_id": request.state.trace_id,
        }
        self.logger.info(
            f"Started request {request.url}", extra={**extra}, stage="start"
        )
        try:
            response = await call_next(request)
        except Exception as exc:
            end_time = datetime.datetime.now()
            time_diff = end_time - start_time
            execution_time = time_diff.total_seconds() * 1000

            self.logger.exception(
                str(exc),
                extra={**extra, "duration": execution_time},
                stage="finish",
            )
            raise exc

        end_time = datetime.datetime.now()
        time_diff = end_time - start_time
        execution_time = time_diff.total_seconds() * 1000

        self.logger.info(
            f"Finished request {request.url}",
            extra={**extra, "duration": execution_time},
            stage="finish",
        )
        response.headers["X-Process-Time"] = str(execution_time)
        return response
