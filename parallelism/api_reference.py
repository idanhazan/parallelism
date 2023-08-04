from __future__ import annotations

from multiprocessing import Process
from os import cpu_count
from threading import Thread
from typing import TYPE_CHECKING

from parallelism.core.handlers.dependency_handler import DependencyHandler
from parallelism.core.executors.process_executor import ProcessExecutor
from parallelism.core.executors.thread_executor import ThreadExecutor
from parallelism.core.scheduled_task import ScheduledTask
from parallelism.core.task_scheduler import TaskScheduler

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Tuple, Type, Union

    from parallelism.core.scheduler_result import SchedulerResult

__all__ = ('scheduled_task', 'task_scheduler')


def scheduled_task(
    executor: Type[Union[Process, Thread]],
    name: str,
    target: Callable[..., Any],
    args: Tuple[Any, ...] = None,
    kwargs: Dict[str, Any] = None,
    *,
    dependencies: Tuple[ScheduledTask, ...] = None,
    priority: Union[int, float] = None,
    processes: int = 0,
    threads: int = 0,
    continual: bool = False,
) -> ScheduledTask:
    """
    The `scheduled_task` function empowers developers to efficiently manage and
    execute tasks in a parallel computing environment.
    It is a fundamental tool for creating and scheduling tasks within the task
    scheduler, allowing for granular control over task execution, dependencies,
    priorities, and result storage.

    Parameters
    ----------
    executor : type of multiprocessing.Process or threading.Thread
        | Specifies the execution unit for the task, either as a
        `multiprocessing.Process` or a `threading.Thread`.
    name : str
        | A unique identifier representing the task, aiding in differentiation
        and tracking.
    target : callable
        | The function to be invoked by the task scheduler upon execution.
    args : tuple, optional
        | Positional arguments related to the `target` function.
    kwargs : dict, optional
        | Keyword arguments related to the `target` function.
    dependencies : tuple of ScheduledTask, optional
        | Tasks that the current task depends on, ensuring proper execution
        order.
    priority : int or float, optional
        | Priority level of task execution, influencing the order of execution
        among tasks.
        | Lower values indicate higher priority.
    processes : int, default 0
        | The number of processes to be allocated by the `target` function.
    threads : int, default 0
        | The number of threads to be allocated by the `target` function.
    continual : bool, default False
        | A flag indicating whether the task scheduler should store the result
        of the task after completion.
        | If `True`, the result is stored for later access.

    Returns
    -------
    ScheduledTask
        A scheduled task instance with configured properties, ready for
        execution within the task scheduler.
    """
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}
    if dependencies is None:
        dependencies = ()
    if priority is None:
        priority = float('inf')
    if not issubclass(executor, (Process, Thread)):
        pattern = 'The {!r} parameter should be of type {!r} or {!r}'
        raise TypeError(pattern.format('executor', 'Process', 'Thread'))
    if not isinstance(name, str):
        pattern = 'The {!r} parameter should be of type {!r}'
        raise TypeError(pattern.format('name', 'str'))
    if not callable(target):
        pattern = 'The {!r} parameter should be a callable object'
        raise TypeError(pattern.format('target'))
    if not isinstance(args, tuple):
        pattern = 'The {!r} parameter should be of type {!r}'
        raise TypeError(pattern.format('args', 'tuple'))
    if not isinstance(kwargs, dict):
        pattern = 'The {!r} parameter should be of type {!r}'
        raise TypeError(pattern.format('kwargs', 'dict'))
    if not isinstance(dependencies, tuple):
        pattern = 'The {!r} parameter should be of type {!r}'
        raise TypeError(pattern.format('dependencies', 'tuple'))
    if not all(isinstance(task, ScheduledTask) for task in dependencies):
        pattern = 'The {!r} parameter only contain {!r}'
        raise TypeError(pattern.format('dependencies', 'ScheduledTask'))
    if not isinstance(priority, (int, float)):
        pattern = 'The {!r} parameter should be of type {!r} or {!r}'
        raise TypeError(pattern.format('priority', 'int', 'float'))
    if not isinstance(processes, int):
        pattern = 'The {!r} parameter should be of type {!r}'
        raise TypeError(pattern.format('processes', 'int'))
    if processes < 0:
        pattern = 'The {!r} parameter should be an integer >= {!r}'
        raise TypeError(pattern.format('processes', 0))
    if not isinstance(threads, int):
        pattern = 'The {!r} parameter should be of type {!r}'
        raise TypeError(pattern.format('threads', 'int'))
    if threads < 0:
        pattern = 'The {!r} parameter should be an integer >= {!r}'
        raise TypeError(pattern.format('threads', 0))
    if not isinstance(continual, bool):
        pattern = 'The {!r} parameter should be of type {!r}'
        raise TypeError(pattern.format('continual', 'bool'))
    if issubclass(executor, Process):
        executor = ProcessExecutor
    if issubclass(executor, Thread):
        executor = ThreadExecutor
    return ScheduledTask(
        executor=executor,
        name=name,
        target=target,
        args=args,
        kwargs=kwargs,
        dependencies=dependencies,
        priority=priority,
        processes=processes,
        threads=threads,
        continual=continual,
        initialized=False,
    )


def task_scheduler(
    tasks: Tuple[ScheduledTask, ...],
    *,
    processes: int = None,
    threads: int = None,
) -> SchedulerResult:
    """
    The `task_scheduler` function orchestrates the simultaneous execution of
    multiple tasks, optimizing parallelism and enhancing computational
    efficiency.
    It allows developers to efficiently manage and distribute tasks among
    processes and threads for improved performance.

    Parameters
    ----------
    tasks : tuple of ScheduledTask
        | A tuple containing instances of ScheduledTask representing the
        tasks to be executed concurrently.
    processes : int, default os.cpu_count()
        | Specifies the total number of parallel processes available for
        executing all tasks collectively.
    threads : int, default os.cpu_count()
        | Specifies the total number of parallel threads available for
        executing all tasks collectively.

    Returns
    -------
    SchedulerResult
        An instance of the `SchedulerResult` class that encapsulates the
        outcomes and statistics of task execution.
        This result provides insights into execution times, elapsed times,
        exceptions, and return values.
    """
    if processes is None:
        processes = cpu_count() or 1
    if threads is None:
        threads = cpu_count() or 1
    if not isinstance(tasks, tuple):
        pattern = 'The {!r} parameter should be of type {!r}'
        raise TypeError(pattern.format('tasks', 'tuple'))
    if not all(isinstance(item, ScheduledTask) for item in tasks):
        pattern = 'The {!r} parameter should only contain {!r}'
        raise TypeError(pattern.format('tasks', 'ScheduledTask'))
    if not len({task.name for task in tasks}) == len(tasks):
        pattern = 'Each {!r} in parameter {!r} should be unique'
        raise TypeError(pattern.format('name', 'tasks'))
    if not DependencyHandler.directed_acyclic_graph(tasks):
        pattern = 'Dependencies of the tasks contains cycles'
        raise TypeError(pattern)
    if not isinstance(processes, int):
        pattern = 'The {!r} parameter should be of type {!r}'
        raise TypeError(pattern.format('processes', 'int'))
    if processes < 0:
        pattern = 'The {!r} parameter should be an integer >= {!r}'
        raise TypeError(pattern.format('processes', 0))
    if not isinstance(threads, int):
        pattern = 'The {!r} parameter should be of type {!r}'
        raise TypeError(pattern.format('threads', 'int'))
    if threads < 0:
        pattern = 'The {!r} parameter should be an integer >= {!r}'
        raise TypeError(pattern.format('threads', 0))
    scheduler = TaskScheduler(tasks, processes, threads)
    return scheduler.execute()
