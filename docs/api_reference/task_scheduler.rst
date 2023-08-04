Task Scheduler
==============

.. autofunction:: parallelism.task_scheduler

.. automodule:: parallelism.core.scheduler_result

   .. py:class:: SchedulerResult

      The `SchedulerResult` class is a specialized container that inherits from the `collections.namedtuple` class,
      designed to hold and manage information related to task scheduling and execution results.
      It encapsulates data about execution times, elapsed times, exceptions, and return values for various tasks.

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

         A dictionary where each key represents a task name, and the corresponding value is the timestamp (`datetime.datetime`) when the task was started.

         >>> ts.execution_time
         {
            'st1': datetime.datetime(%Y, %m, %d, %H, %M, %S, %f),
            'st2': datetime.datetime(%Y, %m, %d, %H, %M, %S, %f),
         }

      .. py:property:: elapsed_time

         A dictionary where each key represents a task name, and the corresponding value is the time in seconds (`float`) it took for the task to complete.

         >>> ts.elapsed_time
         {
            'st1': <time in seconds (float)>,
            'st2': <time in seconds (float)>,
         }

      .. py:property:: raise_exception

         A dictionary where each key represents a task name, and the corresponding value is a `RaiseException` object that contains information about any exceptions raised during task execution.
         The `RaiseException` object has two properties: `exception` (an `Exception` object) and `traceback` (a `str` containing the exception's traceback).

         >>> ts.raise_exception
         {
            'st2': RaiseException(
               exception=Exception('Custom exception message'),
               traceback=<content of traceback (str)>,
            ),
         }

      .. py:property:: return_value

         A dictionary where each key represents a task name, and the corresponding value is the return value (`typing.Any`) from the task's execution after completion.
         Note: `continuous=True` is required.

         >>> ts.return_value
         {
            'st1': 12345,
         }

.. automodule:: parallelism.core.raise_exception

   .. py:class:: RaiseException

      The `RaiseException` class is used within the `SchedulerResult` class to store information about exceptions raised during task execution.

      .. code-block:: python

         from parallelism import scheduled_task, task_scheduler

         def func(a, b):
            return a / b

         st = scheduled_task(executor=..., name='st', target=func, args=(5, 0), ...)
         ts = task_scheduler(tasks=(st,), ...)

      .. py:property:: exception

         The exception object that was raised during task execution.

         >>> ts.raise_exception.get('st').exception
         ZeroDivisionError: division by zero

      .. py:property:: traceback

         A string representation of the traceback associated with the raised exception.

         >>> ts.raise_exception.get('st').traceback
         Traceback (most recent call last):
           File ".../site-packages/parallelism/core/handlers/function_handler.py", line ..., in __call__
             self.proxy['return_value'] = self.target(*args, **kwargs)
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
           File ".../main.py", line ..., in func
             return a / b
                    ^^^^^
         ZeroDivisionError: division by zero

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
