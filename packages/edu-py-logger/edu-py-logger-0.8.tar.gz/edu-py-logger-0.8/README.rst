edu-py-logger
=============

Version
    0.3

Download
    https://pypi.org/project/edu-py-logger/

Keywords
    logging, fastapi, python

Installation
------------

To install, please use ``pip``:

::

    pip install edu-py-logger

Connection and configuration
----------------------------

Logger connects in the settings with 2 strings:

::

    dictConfig(get_config(settings.service_name, settings.logging_file_path))
    settings.logger = LoggerService(settings.service_name, settings.run_env)

Add to settings new attribute logging\_file\_path to configure path for
output file. The path for output is set up in env.

::

    LOGGING_FILE_PATH=/home/dev/logging.log

Log format
----------

::

    (
        "%(service_name)s | "
        "%(ipv4)s | "
        "%(env)s | "
        "%(trace_id)s | "
        "%(correlation_id)s | "
        "%(user_id)s | "
        "%(levelprefix)s | "
        "%(asctime)s | "
        "%(message)s"
    )

FastAPI integration:
--------------------

Please use ``TraceIdProcessTimeMiddleware`` to create ``trace_id`` in
request state.

::

    from fastapi import FastAPI
    from edu_py_logger.middlewares import TraceIdProcessTimeMiddleware

    app = FastAPI()
    app.add_middleware(TraceIdProcessTimeMiddleware)

To create extra from request, please use util
``get_request_extra_data``.

Example:

::

    from typing import Dict
    from edu_py_logger.utils import get_request_extra_data
    from fastapi import APIRouter, Depends
    from app.config import settings

    router = APIRouter()


    @router.get("/test")
    def test(extra: Dict = Depends(get_request_extra_data)):
        settings.logger.info('message', extra=extra)

Package tests
-------------

To run test:

::

    pytest
