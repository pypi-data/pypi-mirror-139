from edu_py_logger.utils import PropertyBaseModel


class LogConfig(PropertyBaseModel):
    """Logging configuration to be set for the server"""

    logger_name: str
    log_level: str = "DEBUG"
    version = 1
    file_path: str = None
    disable_existing_loggers = False
    formatters = {
        "ecs": {
            "()": "ecs_logging.StdlibFormatter",
            "exclude_fields": [
                "log",
                "process",
            ],
        }
    }

    @property
    def handlers(self):
        return {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "ecs",
            },
            "file": {
                "formatter": "ecs",
                "class": "logging.FileHandler",
                "filename": self.file_path or f"{self.logger_name}.log",
            },
        }

    @property
    def loggers(self):
        if self.file_path:
            loggers = ["console", "file"]
        else:
            loggers = ["console"]
        return {
            self.logger_name: {
                "handlers": loggers,
                "level": "DEBUG",
            }
        }


def get_config(name, path=None):
    return LogConfig(logger_name=name, file_path=path).dict()
