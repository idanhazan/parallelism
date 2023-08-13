# parallelism

Unlock advanced task scheduling in Python with `parallelism`.
Seamlessly coordinate parallel and concurrent execution, optimizing performance while ensuring code integrity.
Embrace expert scheduling techniques to elevate your programming to new heights of efficiency and responsiveness.

## Installation

You can install this package using pip:

```bash
pip install parallelism
```

## Basic Usage

Explore an effortless approach to task creation and management.
Follow these steps to get started:

1. Import the necessary classes and functions in your Python code.

  ```python
  # Built-in modules
  from multiprocessing import Process
  from threading import Thread

  # Third-party libraries
  from parallelism import scheduled_task, task_scheduler
  ```

2. Define your task functions. These user-defined functions will be executed in parallel and concurrently.

```python
def func(*args, **kwargs):
    if not args and not kwargs:
        raise ValueError('Missing *args or **kwargs')
    return args, kwargs
```

3. Create task instances using the `scheduled_task` function, specifying the execution unit (Process or Thread), task name, function, and provide any required positional or keyword arguments.

```python
task1 = scheduled_task(Process, 'task1', func, args=(1, 2, 3), continual=True)
task2 = scheduled_task(Process, 'task2', func, kwargs={'a': 10, 'b': 20}, continual=True)
task3 = scheduled_task(Thread, 'task3', func, continual=True)
```

4. Schedule tasks using the `task_scheduler` function, Specify the tasks to be executed along with the desired number of processes and threads.

```python
result = task_scheduler(tasks=(task1, task2, task3), processes=2, threads=4)
```

5. Access task execution details and results through the result object, providing insights into execution times, elapsed times, exceptions, and return values:

```python
>>> result.execution_time
{
    'task1': datetime.datetime(%Y, %m, %d, %H, %M, %S, %f),
    'task2': datetime.datetime(%Y, %m, %d, %H, %M, %S, %f),
    'task3': datetime.datetime(%Y, %m, %d, %H, %M, %S, %f),
}
>>> result.elapsed_time
{
    'task1': float(...),
    'task2': float(...),
    'task3': float(...),
}
>>> result.raise_exception
{
    'task3': ValueError('Missing *args or **kwargs'),
}
>>> result.return_value
{
    'task1': ((1, 2, 3), {}),
    'task2': ((), {'a': 10, 'b': 20}),
}
```

For more comprehensive documentation and advanced usage, please refer to the full [API Documentation](https://parallelism.readthedocs.io/en/latest/index.html).
