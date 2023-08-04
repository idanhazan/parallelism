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

      Accessing a Return Value:

      >>> st1.return_value
      ReturnValue(task=ScheduledTask(executor=..., name='st1', target='__main__.func1', ...))
      # At runtime: 12345

      .. py:method:: __call__(self, *args, **kwargs)

         Invokes the `ReturnValue` object as a callable.
         This method is used to retrieve the actual return value of the scheduled task.

         Invoking the Return Value as a Callable:

         >>> st2.return_value()
         ReturnValue(task=ScheduledTask(executor=..., name='st2', target='__main__.func2', ...)))
         # At runtime: 12345

         Invoking the Return Value with Parameters:

         >>> st2.return_value(reverse=True)
         ReturnValue(task=ScheduledTask(executor=..., name='st2', target='__main__.func2', ...)))
         # At runtime: 54321

      .. py:method:: __getattribute__(self, name)

         Retrieves an attribute or method of the actual return value.
         This method allows access to properties and methods of the return value without directly referencing it.

         Accessing a Specific Key in the Return Dictionary:

         >>> st3.return_value.get('b')
         ReturnValue(task=ScheduledTask(executor=..., name='st3', target='__main__.func3', ...))
         # At runtime: 45

      .. py:method:: __getitem__(self, key)

         Retrieves an item from the actual return value using the provided key.
         This method allows accessing elements of the return value, such as lists, dictionaries, etc.

         Accessing an Element by Index:

         >>> st4.return_value[2]
         ReturnValue(task=ScheduledTask(executor=..., name='st4', target='__main__.func4', ...)))
         # At runtime: 3

         Accessing a Slice of Elements:

         >>> st4.return_value[3:]
         ReturnValue(task=ScheduledTask(executor=..., name='st4', target='__main__.func4', ...)))
         # At runtime: 45

Examples
--------

.. code-block:: python

   # Built-in modules
   from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
   from multiprocessing import Process
   from threading import Thread
   
   # Third-party packages
   from parallelism import scheduled_task

Executor
********

Running Different Concurrent Environments:

In this example, `scheduled_task` is used to create a scheduled task named `p` that runs as a `multiprocessing.Process`,
and another task named `t` that runs as a `threading.Thread`.
Both tasks execute the same function, `func`.

>>> def func():
...     pass
...
>>> p = scheduled_task(Process, 'p', func)
>>> t = scheduled_task(Thread, 't', func)

Args & Kwargs
*************

Passing Arguments and Dependencies:

Here, `scheduled_task` demonstrates passing arguments and dependencies.
`p` calculates the sum of `1 + 2 + 3`, and `t` uses the return value of `p` as an argument.

>>> def func1(a, b, c):
...     return a + b + c
...
>>> def func2(x):
...     print(x)
...
>>> p = scheduled_task(Process, 'p', func1, args=(1, 2), kwargs={'c': 3})
>>> t = scheduled_task(Thread, 't', func2, kwargs={'x': p.return_value})

Dependencies
************

Managing Task Dependencies:

This example showcases task dependencies.
`t` depends on the completion of `p` before starting its execution.

>>> def func1(path, text):
...     with open(path, 'w') as file:
...         file.write(text)
...
>>> def func2(path):
...     with open(path, 'r') as file:
...         return file.read()
...
>>> p = scheduled_task(Process, 'p', func1, kwargs={'path': 'example.txt', 'text': 'Hello, World!'})
>>> t = scheduled_task(Thread, 't', func2, kwargs={'path': 'example.txt'}, dependencies=(p,))

Priority
********

Setting Task Priority:

In this scenario, tasks are assigned priorities.
`t` is given higher priority than `p`, affecting their order of execution.

>>> def func():
...     pass
...
>>> p = scheduled_task(Process, 'p', func, priority=2)
>>> t = scheduled_task(Thread, 't', func, priority=1)

Processes & Threads
*******************

Balancing Processes and Threads:

Here, `scheduled_task` is used to distribute workload across processes and threads based on specified weights.

>>> def func():
...     with ProcessPoolExecutor(max_workers=2) as executor:
...         pass
...     with ThreadPoolExecutor(max_workers=4) as executor:
...         pass
...
>>> p = scheduled_task(Process, 'p', func, processes=2, threads=4)

Continual
*********

Storing Task Return Values:

This example illustrates how to manage stored return values.
`p`'s return value is stored due to the `continual=True` parameter, while `t`'s return value is not stored.

>>> def func():
...     return 123
...
>>> p = scheduled_task(Process, 'p', func, continual=True)
>>> t = scheduled_task(Thread, 't', func, continual=False)
