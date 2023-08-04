Scheduled Task
==============

.. autofunction:: parallelism.scheduled_task

.. automodule:: parallelism.core.scheduled_task

   .. py:class:: ScheduledTask

      The `ScheduledTask` class, a subclass of `collections.namedtuple`, represents a scheduled task along with its associated return value.
      This class provides a mechanism to access the return value of the task in a deferred manner using the `ReturnValue` object.

      .. py:property:: return_value

         A reference to the ReturnValue object associated with this scheduled task.
         The `ReturnValue` object provides deferred access to the actual return value of the task.

.. automodule:: parallelism.core.return_value

   .. py:class:: ReturnValue

      The `ReturnValue` class represents a deferred reference to the return value of a scheduled task.
      It implements the `__call__`, `__getattribute__`, and `__getitem__` methods to provide flexible access to the actual return value.

      .. code-block:: python
      
         from parallelism import scheduled_task

         def func1(reverse=False):
            return 54321 if reverse else 12345

         def func2():
            return func1

         def func3():
            return {'a': 123, 'b': 45}

         def func4():
            return [1, 2, 3, 4, 5]

         st1 = scheduled_task(executor=..., name='st1', target=func1, ...)
         st2 = scheduled_task(executor=..., name='st2', target=func2, ...)
         st3 = scheduled_task(executor=..., name='st3', target=func3, ...)
         st4 = scheduled_task(executor=..., name='st4', target=func4, ...)

      >>> st1.return_value
      ReturnValue(task=ScheduledTask(executor=..., name='st1', target='__main__.func1', ...))

      In this case, the return value will be `12345`

      .. py:method:: __call__(self, *args, **kwargs)

         Invokes the `ReturnValue` object as a callable.
         This method is used to retrieve the actual return value of the scheduled task.

         >>> st2.return_value()
         ReturnValue(task=ScheduledTask(executor=..., name='st2', target='__main__.func2', ...)))

         In this case, the return value will be `12345`

         >>> st2.return_value(reverse=True)
         ReturnValue(task=ScheduledTask(executor=..., name='st2', target='__main__.func2', ...)))

         In this case, the return value will be `54321`

      .. py:method:: __getattribute__(self, name)

         Retrieves an attribute or method of the actual return value.
         This method allows access to properties and methods of the return value without directly referencing it.

         >>> st3.return_value.get('b')
         ReturnValue(task=ScheduledTask(executor=..., name='st3', target='__main__.func3', ...))

         In this case, the return value will be `45`

      .. py:method:: __getitem__(self, key)

         Retrieves an item from the actual return value using the provided key.
         This method allows accessing elements of the return value, such as lists, dictionaries, etc.

         >>> st4.return_value[2]
         ReturnValue(task=ScheduledTask(executor=..., name='st4', target='__main__.func4', ...)))

         In this case, the return value will be `3`

         >>> st4.return_value[3:]
         ReturnValue(task=ScheduledTask(executor=..., name='st4', target='__main__.func4', ...)))

         In this case, the return value will be `45`

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
