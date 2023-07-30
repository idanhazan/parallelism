scheduled_task
==============

.. autofunction:: parallelism.scheduled_task

Examples
--------

.. code-block:: python

    # Built-in modules
    from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
    from multiprocessing import Process
    from threading import Thread

    # Third-party packages
    from parallelism import scheduled_task

An example of basic use (very similar to the original):

>>> def func(a, b, c):
...     return a + b + c
...
>>> # Similar to: multiprocessing.Process(target=func, name='p', args=(1, 2), kwargs={'c': 3})
>>> scheduled_task(executor=Process, name='p', target=func, args=(1, 2), kwargs={'c': 3})
ScheduledTask(executor='Process', name='p', target='__main__.func', args=2, kwargs=1, dependencies=0, priority=inf, processes=0, threads=0, continual=False)
>>> # Similar to: threading.Thread(target=func, name='t', args=(1, 2), kwargs={'c': 3})
>>> scheduled_task(executor=Thread, name='t', target=func, args=(1, 2), kwargs={'c': 3})
ScheduledTask(executor='Thread', name='t', target='__main__.func', args=2, kwargs=1, dependencies=0, priority=inf, processes=0, threads=0, continual=False)
