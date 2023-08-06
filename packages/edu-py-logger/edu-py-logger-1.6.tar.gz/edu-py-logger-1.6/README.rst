edu-py-logger
=============

Version
   1.6
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
   settings.logger = LoggerService(
       service_name=settings.service_name,
       service_version=settings.service_version,
       env=environments.get(settings.run_env, 'test'),
   )

Add to settings new attribute logging_file_path to configure path for
output file. The path for output is set up in env.

::

   LOGGING_FILE_PATH=/home/dev/logging.log

Log format example
------------------

::

   {
     "@timestamp": "2022-02-18T13:29:37.389Z",
     "message": "Get tutor popular micro lessons from 2021-01-31 to 2022-06-12",
     "correlation_id": "d794ef71-e9d6-45cf-992e-324a9bc49870",
     "current_action": "/analytics/tutor/popular/microlesson",
     "ecs": {
       "version": "1.6.0"
     },
     "env": "local",
     "ipv4": "127.0.1.1",
     "ipv6": "",
     "root_action": "/analytics/tutor/popular/microlesson",
     "service_name": "edu-user-analytics-service",
     "service_version": "1.0",
     "trace_id": "65e76724-d8a0-4e03-840e-fca72f672cae",
     "user_id": "60b7588b2206860013e77aa8",
     "transaction_id": "transaction_id",
     "span_id": "span_id"
   }

FastAPI integration:
--------------------

Please use ``TraceIdProcessTimeMiddleware`` to create ``trace_id`` in
request state.

.. code:: python

   from fastapi import FastAPI
   from edu_py_logger.middlewares import TraceIdProcessTimeMiddleware
   from app.config import settings

   app = FastAPI()
   app.add_middleware(TraceIdProcessTimeMiddleware, logger=settings.logger)

To create extra from request, please use util
``get_request_extra_data``.

Example:

.. code:: python

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

Update and publish package:
---------------------------

1) change package version in ``setup.py`` file
2) run command to build package:

::

   python setup.py sdist

3) run command to upload new version on PyPI:

::

   twine upload dist/edu-py-logger-0.4.tar.gz
