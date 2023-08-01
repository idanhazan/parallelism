scheduled_task
==============

.. automodule:: parallelism

.. autofunction:: parallelism.scheduled_task

Information
-----------

The `scheduled_task` function returns a `ScheduledTask` object,
this object has a property called `return_value` which returns a `ReturnValue` object.

The ReturnValue object implements `__call__`, `__getattribute__` and `__getitem__`
to allow getting the desired value at runtime.

>>> st = scheduled_task(...)
>>> # As it is without change
>>> st.return_value
ReturnValue(task=ScheduledTask(...))
>>> # __call__
>>> st.return_value(*args, **kwargs)
ReturnValue(task=ScheduledTask(...))
>>> # __getattribute__
>>> st.return_value.name
ReturnValue(task=ScheduledTask(...))
>>> # __getitem__
>>> st.return_value[key]
ReturnValue(task=ScheduledTask(...))

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
