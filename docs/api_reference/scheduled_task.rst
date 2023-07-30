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

An example of basic usage for creating a `Process` and/or `Thread`:

>>> def func():
...     pass
...
>>> scheduled_task(Process, 'p', func)
ScheduledTask(executor='Process', name='p', target='__main__.func', args=2, kwargs=1, dependencies=0, priority=inf, processes=0, threads=0, continual=False)
>>> scheduled_task(Thread, 't', func)
ScheduledTask(executor='Thread', name='t', target='__main__.func', args=2, kwargs=1, dependencies=0, priority=inf, processes=0, threads=0, continual=False)

An example of basic usage for `args` and `kwargs`:

>>> def func1(a, b, c):
...     return a + b + c
...
>>> def func2(x):
...     print(x)
...
>>> p = scheduled_task(Process, 'p', func1, args=(1, 2), kwargs={'c': 3})
>>> t = scheduled_task(Thread, 't', func2, kwargs={'x': p.return_value})
