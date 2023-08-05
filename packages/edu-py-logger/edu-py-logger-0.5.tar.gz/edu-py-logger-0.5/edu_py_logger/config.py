from typing import Dict

from edu_py_logger.utils import PropertyBaseModel


class LogConfig(PropertyBaseModel):
    """Logging configuration to be set for the server"""
    logger_name: str
    log_level: str = "DEBUG"
    version = 1

    disable_existing_loggers = False
    formatters = {
        "ecs": {
            "()": "ecs_logging.StdlibFormatter"
        }
    }
    handlers: Dict = {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "ecs",
        },
        "file": {
            "formatter": "ecs",
            'class': 'logging.FileHandler',
            'filename': 'logging_path.log',
        }
    }

    @property
    def loggers(self):
        return {
            self.logger_name: {
                "handlers": ["console", "file"],
                "level": "DEBUG"
            }
        }


def get_config(name):
    return LogConfig(logger_name=name).dict()
