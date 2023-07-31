scheduled_task
==============

.. autofunction:: parallelism.scheduled_task

.. autoclass:: parallelism.core.scheduled_task.ScheduledTask

   .. autoproperty:: return_value

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
>>> p = scheduled_task(Process, 'p', func)
>>> t = scheduled_task(Thread, 't', func)

An example of basic usage for `args` and `kwargs`:

>>> def func1(a, b, c):
...     return a + b + c
...
>>> def func2(x):
...     print(x)
...
>>> p = scheduled_task(Process, 'p', func1, args=(1, 2), kwargs={'c': 3})
>>> t = scheduled_task(Thread, 't', func2, kwargs={'x': p.return_value})

An example of basic usage for `dependencies`:

>>> def func1():
...     # Saving a local file or updating a database record
...
>>> def func2():
...     # Reading a local file or retrieving a record from the database
...
>>> p = scheduled_task(Process, 'p', func1)
>>> t = scheduled_task(Thread, 't', func2, dependencies=(p,))

An example of basic usage for `processes` and `threads`:

>>> def func():
...     with ProcessPoolExecutor(max_workers=2) as executor:
...         pass
...     with ThreadPoolExecutor(max_workers=4) as executor:
...         pass
...
>>> p = scheduled_task(Process, 'p', func, processes=2, threads=4)
