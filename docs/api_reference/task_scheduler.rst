Task Scheduler
==============

.. autofunction:: parallelism.task_scheduler

.. automodule:: parallelism.core.scheduler_result

   .. py:class:: SchedulerResult

      # Coming soon...

      .. py:property:: elapsed_time

         # Coming soon...

      .. py:property:: error_handler

         # Coming soon...

      .. py:property:: return_value

         # Coming soon...

.. automodule:: parallelism.core.handlers.error_handler

   .. py:class:: ErrorHandler

      # Coming soon...

      .. py:property:: exception

         # Coming soon...

      .. py:property:: traceback

         # Coming soon...

Examples
--------

.. code-block:: python

   # Built-in modules
   from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
   from multiprocessing import Process
   from threading import Thread

   # Third-party packages
   from parallelism import scheduled_task, task_scheduler

Example of ...:

>>> task_scheduler(...)
...
