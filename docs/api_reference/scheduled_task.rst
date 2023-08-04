Scheduled Task
==============

.. autofunction:: parallelism.scheduled_task

.. automodule:: parallelism.core.scheduled_task

   .. py:class:: ScheduledTask

      A :py:obj:`collections.namedtuple` object representing a task

      .. py:property:: return_value

         An object containing a reference to the return value of a task

.. automodule:: parallelism.core.return_value

   .. py:class:: ReturnValue

      This object implements
      `__call__`, `__getattribute__` and `__getitem__`
      to allow getting the desired value at runtime

      .. code-block:: python
      
         from parallelism import scheduled_task

         st = scheduled_task(executor=..., name=..., target=..., args, kwargs, ...)

      >>> st.return_value
      ReturnValue(task=ScheduledTask(...))

      .. py:method:: __call__(self, *args, **kwargs)

         >>> st.return_value(*args, **kwargs)
         ReturnValue(task=ScheduledTask(...))

      .. py:method:: __getattribute__(self, name)

         >>> st.return_value.name
         ReturnValue(task=ScheduledTask(...))

      .. py:method:: __getitem__(self, key)

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

Minimalistic
************

An example of basic usage for creating a `ScheduledTask` instances:

>>> def func():
...     pass
...
>>> p = scheduled_task(Process, 'p', func)
>>> t = scheduled_task(Thread, 't', func)

In this case, both `p` and `t` will be the same except that `p` will run as `multiprocessing.Process` and `t` will run as `threading.Thread`

Parameters
**********

An example of basic usage for `args` and `kwargs`:

>>> def func1(a, b, c):
...     return a + b + c
...
>>> def func2(x):
...     print(x)
...
>>> p = scheduled_task(Process, 'p', func1, args=(1, 2), kwargs={'c': 3})
>>> t = scheduled_task(Thread, 't', func2, kwargs={'x': p.return_value})

In this case, `t` will start only after `p` completed, and the parameter `x` will be equal to `6`

Dependencies
************

An example of basic usage for `dependencies`:

>>> def func1():
...     # Saving a local file or updating a database record
...
>>> def func2():
...     # Reading a local file or retrieving a record from the database
...
>>> p = scheduled_task(Process, 'p', func1)
>>> t = scheduled_task(Thread, 't', func2, dependencies=(p,))

In this case, `t` will start only after `p` completed

Priorities
**********

An example of basic usage for `priority`:

>>> def func():
...     pass
...
>>> p = scheduled_task(Process, 'p', func, priority=2)
>>> t = scheduled_task(Thread, 't', func, priority=1)

In this case, `t` will be prioritize over `p`

Workers
*******

An example of basic usage for `processes` and `threads`:

>>> def func():
...     with ProcessPoolExecutor(max_workers=2) as executor:
...         pass
...     with ThreadPoolExecutor(max_workers=4) as executor:
...         pass
...
>>> p = scheduled_task(Process, 'p', func, processes=2, threads=4)

In this case, 'p' will get additional weight of number of processes and threads

Continuity
**********

An example of basic usage for `continual`:

>>> def func():
...     return 123
...
>>> p = scheduled_task(Process, 'p', func, continual=True)
>>> t = scheduled_task(Thread, 't', func, continual=False)

In this case, when the task scheduler will complete, it will store only the return value of `p`
