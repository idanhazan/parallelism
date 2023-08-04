Task Scheduler
==============

.. autofunction:: parallelism.task_scheduler

.. automodule:: parallelism.core.scheduler_result

   .. py:class:: SchedulerResult

      This object contains all the required information that occurred for each task

      .. code-block:: python

         from parallelism import scheduled_task, task_scheduler

         def func1():
            return 12345

         def func2():
            raise Exception('Custom exception message')

         st1 = scheduled_task(executor=..., name='st1', target=func1, ..., continual=True)
         st2 = scheduled_task(executor=..., name='st2', target=func2, ..., continual=True)
         ts = task_scheduler(tasks=(st1, st2), ...)

      .. py:property:: execution_time

         >>> ts.execution_time
         {
            'st1': datetime.datetime(%Y, %m, %d, %H, %M, %S, %f),
            'st2': datetime.datetime(%Y, %m, %d, %H, %M, %S, %f),
         }

      .. py:property:: elapsed_time

         >>> ts.elapsed_time
         {
            'st1': <time in seconds (float)>,
            'st2': <time in seconds (float)>,
         }

      .. py:property:: error_handler

         >>> ts.error_handler
         {
            'st2': ErrorHandler(
               exception=Exception('Custom exception message'),
               traceback=<string of traceback>,
            ),
         }

      .. py:property:: return_value

         >>> ts.return_value
         {
            'st1': 12345,
         }

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
