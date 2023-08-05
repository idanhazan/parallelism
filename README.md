# parallelism

The Parallelism library offers a powerful set of tools for managing concurrent task execution using both processes and threads.
It aims to simplify the development of parallel programs, providing a higher-level interface for distributing tasks across multiple execution units.
Whether your tasks are CPU-bound or I/O-bound, the Parallelism library facilitates efficient and streamlined parallel processing.

## Installation

You can install the Parallelism library using pip:

```bash
pip install parallelism
```

## Basic Usage

The Parallelism library offers an intuitive way to create and manage tasks for concurrent execution.
Here's a simple example of how to use the library:

1. Import the necessary modules and classes in your Python code:

  ```python
  from multiprocessing import Process
  from threading import Thread
  
  from parallelism import scheduled_task, task_scheduler
  ```

2. Define your task functions. These functions will be executed concurrently:

```python
def func(*args, **kwargs):
    # Your task logic here
    pass
```

3. Create task instances using the `scheduled_task` function, specifying the execution unit (Process or Thread), task name, function, and positional arguments or keyword arguments:

```python
task1 = scheduled_task(Process, 'task1', func, args=(...))
task2 = scheduled_task(Thread, 'task2', func, kwargs={...})
```

4. Schedule tasks using the `task_scheduler` function, indicating the tasks to be executed and the desired number of processes and threads:

```python
result = task_scheduler(tasks=(task1, task2), processes=2, threads=4)
```

5. Access task execution details and results through the result object, providing insights into execution times, elapsed times, exceptions, and return values:

```python
result.execution_time
result.elapsed_time
result.raise_exception
result.return_value
```

For more comprehensive documentation and advanced usage, please refer to the full [API Documentation](https://parallelism.readthedocs.io/en/latest/index.html).
