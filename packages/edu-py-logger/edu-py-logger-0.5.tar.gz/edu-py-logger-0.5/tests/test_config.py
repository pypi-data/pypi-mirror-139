from unittest import TestCase

from edu_py_logger.config import get_config


class TestLogger(TestCase):
    def test_get_config(self):
        expected = {
            'logger_name': 'name',
            'log_level': 'DEBUG',
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                    'formatter': 'ecs'
                },
                'file': {
                    'formatter': 'ecs',
                    'class': 'logging.FileHandler',
                    'filename': 'logging_path.log'
                }
            },
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'ecs': {
                    '()': 'ecs_logging.StdlibFormatter'
                }
            },
            'loggers': {
                'name': {
                    'handlers': ['console', 'file'],
                    'level': 'DEBUG'
                }
            }
        }

        result = get_config("name")
        print(result)
        self.assertEqual(result, expected)
