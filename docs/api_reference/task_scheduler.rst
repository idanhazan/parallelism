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
         ZeroDivisionError('division by zero')

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

Example #1:

>>> from operator import add, mul
...
>>> def func1(operator, a, b):
...     return operator(a, b)
...
>>> def func2(value):
...     return str(value)
...
>>> def func3(values):
...     return sorted(values)
...
>>> p1 = scheduled_task(Process, 'p1', func1, (add, 3, 1), priority=1)
>>> p2 = scheduled_task(Process, 'p2', func1, (mul, 3, 1), priority=3)
>>> p3 = scheduled_task(Process, 'p3', func1, (add, 3, 'w'), priority=2)
>>> p4 = scheduled_task(Process, 'p4', func1, (mul, 3, 'w'), priority=4)
...
>>> t1 = scheduled_task(Thread, 't1', func2, (p1.return_value,), continual=True)
>>> t2 = scheduled_task(Thread, 't2', func2, (p2.return_value,), continual=True)
>>> t3 = scheduled_task(Thread, 't3', func2, (p3.return_value,), continual=True)
>>> t4 = scheduled_task(Thread, 't4', func2, (p4.return_value,), continual=True)
...
>>> s1 = task_scheduler(tasks=(p1, p2, p3, p4, t1, t2, t3, t4), processes=2, threads=2)
...
TIMESTAMP [INFO] [parallelism:PID:TID] - 'p1' ran approximately ... nanoseconds
TIMESTAMP [ERROR] [parallelism:PID:TID] - 'p3' ran approximately ... milliseconds - TypeError("unsupported operand type(s) for +: 'int' and 'str'")
TIMESTAMP [WARNING] [parallelism:PID:TID] - 't3' is being canceled, due to task 'p3'
TIMESTAMP [INFO] [parallelism:PID:TID] - 'p2' ran approximately ... nanoseconds
TIMESTAMP [INFO] [parallelism:PID:TID] - 't1' ran approximately ... nanoseconds
TIMESTAMP [INFO] [parallelism:PID:TID] - 'p4' ran approximately ... nanoseconds
TIMESTAMP [INFO] [parallelism:PID:TID] - 't2' ran approximately ... nanoseconds
TIMESTAMP [INFO] [parallelism:PID:TID] - 't4' ran approximately ... nanoseconds
...
>>> s1.execution_time
{
    'p1': datetime.datetime(...),
    'p3': datetime.datetime(...),
    't3': datetime.datetime(...),
    'p2': datetime.datetime(...),
    't1': datetime.datetime(...),
    'p4': datetime.datetime(...),
    't2': datetime.datetime(...),
    't4': datetime.datetime(...),
}
>>> s1.elapsed_time
{
    'p1': ...,
    'p3': ...,
    'p2': ...,
    't1': ...,
    'p4': ...,
    't2': ...,
    't4': ...,
}
>>> s1.raise_exception
{
    'p3': TypeError("unsupported operand type(s) for +: 'int' and 'str'"),
    't3': DependencyError("'t3' has been canceled", ('p3',)),
}
>>> s1.return_value
{
    't1': '4',
    't2': '3',
    't4': 'www',
}
...
>>> p5 = scheduled_task(Process, 'p5', func3, (s1.return_value.values(),), continual=True)
...
>>> s2 = task_scheduler(tasks=(p5,), processes=1, threads=0)
...
TIMESTAMP [INFO] [parallelism:PID:TID] - 'p5' ran approximately ... milliseconds
...
>>> s2.execution_time
{
    'p5': datetime.datetime(...),
}
>>> s2.elapsed_time
{
    'p5': ...,
}
>>> s2.raise_exception
{
}
>>> s2.return_value
{
    'p5': ['3', '4', 'www'],
}
