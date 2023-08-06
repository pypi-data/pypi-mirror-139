from unittest import TestCase

from edu_py_logger.config import get_config


class TestLogger(TestCase):
    def test_get_config_with_file(self):
        expected = {
            "logger_name": "name",
            "log_level": "DEBUG",
            "file_path": "logging_path.log",
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "ecs",
                },
                "file": {
                    "formatter": "ecs",
                    "class": "logging.FileHandler",
                    "filename": "logging_path.log",
                },
            },
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "ecs": {
                    "()": "ecs_logging.StdlibFormatter",
                    "exclude_fields": [
                        "log",
                        "process",
                    ],
                },
            },
            "loggers": {
                "name": {"handlers": ["console", "file"], "level": "DEBUG"}
            },
        }

        result = get_config("name", "logging_path.log")
        self.assertEqual(result, expected)

    def test_get_config(self):
        expected = {
            "logger_name": "name",
            "log_level": "DEBUG",
            "file_path": None,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "ecs",
                },
                "file": {
                    "formatter": "ecs",
                    "class": "logging.FileHandler",
                    "filename": "name.log",
                },
            },
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "ecs": {
                    "()": "ecs_logging.StdlibFormatter",
                    "exclude_fields": [
                        "log",
                        "process",
                    ],
                }
            },
            "loggers": {"name": {"handlers": ["console"], "level": "DEBUG"}},
        }

        result = get_config("name")
        self.assertEqual(result, expected)
