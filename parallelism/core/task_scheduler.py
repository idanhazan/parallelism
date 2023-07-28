from __future__ import annotations

from multiprocessing import Manager, Process
from threading import Thread
from typing import TYPE_CHECKING

from parallelism.core.handlers.dependency_handler import DependencyHandler
from parallelism.core.handlers.function_handler import FunctionHandler
from parallelism.core.handlers.parameters_handler import ParametersHandler
from parallelism.core.handlers.shared_memory_handler import SharedMemoryHandler
from parallelism.core.scheduled_task import ScheduledTask
from parallelism.core.scheduler_result import SchedulerResult

if TYPE_CHECKING:
    from typing import Literal, Tuple

__all__ = ('TaskScheduler',)


class TaskScheduler:
    __slots__ = (
        'tasks',
        'returns',
        'processes',
        'threads',
        'manager',
        'proxy',
        'dependency_handler',
        'shared_memory_handler',
    )

    def __init__(
        self,
        tasks: Tuple[ScheduledTask, ...],
        processes: int,
        threads: int,
    ) -> None:
        self.tasks = sorted(tasks, key=lambda task: task.priority)
        self.processes = processes
        self.threads = threads
        self.manager = None
        self.proxy = None
        self.dependency_handler = None
        self.shared_memory_handler = None

    @property
    def finished(self) -> bool:
        return all(
            task.initialized and
            self.proxy.get(task.name).get('finish')
            for task in self.tasks
        )

    @property
    def active_tasks(self) -> Tuple[ScheduledTask, ...]:
        return tuple(
            task for task in self.tasks
            if (
                task.initialized and
                self.proxy.get(task.name).get('start') and not
                self.proxy.get(task.name).get('finish')
            )
        )

    @property
    def active_processes(self) -> int:
        return sum(
            task.processes + (1 if isinstance(task.executor, Process) else 0)
            for task in self.active_tasks
        )

    @property
    def active_threads(self) -> int:
        return sum(
            task.threads + 1 if isinstance(task.executor, Thread) else 0
            for task in self.active_tasks
        )

    def execute(self) -> SchedulerResult:
        self.manager = Manager()
        self.proxy = self.manager.dict()
        self.dependency_handler = DependencyHandler(
            tasks=self.tasks,
            proxy=self.proxy,
        )
        self.shared_memory_handler = SharedMemoryHandler(
            tasks=self.tasks,
            proxy=self.proxy,
            prerequisites=self.dependency_handler.prerequisites,
        )
        for index, task in enumerate(self.tasks):
            if not self.enough_workers(task):
                self.proxy[task.name] = self.manager.dict()
                task = self.initialize(task, blocked='worker')
                self.tasks[index] = task
        while not self.finished:
            for index, task in enumerate(self.tasks):
                if task.initialized:
                    self.shared_memory_handler.free(task)
                    continue
                if not self.available_worker(task):
                    continue
                if self.dependency_handler.is_blocked(task, status='finish'):
                    continue
                if self.dependency_handler.is_blocked(task, status='complete'):
                    self.proxy[task.name] = self.manager.dict()
                    task = self.initialize(task, blocked='dependency')
                    self.tasks[index] = task
                    continue
                self.proxy[task.name] = self.manager.dict()
                task = self.initialize(task)
                self.tasks[index] = task
                task.executor.start()
                break
        for task in self.tasks:
            self.shared_memory_handler.free(task)
        self.manager.shutdown()
        return SchedulerResult(
            self.shared_memory_handler.elapsed_time,
            self.shared_memory_handler.error_handler,
            self.shared_memory_handler.return_value,
        )

    def initialize(
        self,
        task: ScheduledTask,
        blocked: Literal['dependency', 'worker'] = None,
    ) -> ScheduledTask:
        full_proxy = self.proxy
        partial_proxy = self.proxy.get(task.name)
        blocker = None
        if blocked == 'dependency':
            tasks = self.dependency_handler.blocking_tasks(task)
            blocker = {'reason': blocked, 'tasks': tasks}
        if blocked == 'worker':
            processes = 0
            threads = 0
            if task.executor.__base__ == Process:
                processes = abs(min(0, self.processes - (task.processes + 1)))
                threads = abs(min(0, self.threads))
            if task.executor.__base__ == Thread:
                processes = abs(min(0, self.processes - task.processes))
                threads = abs(min(0, self.threads - (task.threads + 1)))
            blocker = {'reason': blocked, 'processes': processes, 'threads': threads}
        function_handler = FunctionHandler(
            name=task.name,
            target=task.target,
            proxy=partial_proxy,
            blocker=blocker,
        )
        if blocked:
            args = task.args
            kwargs = task.kwargs
        else:
            parameters_handler = ParametersHandler(proxy=full_proxy)
            args = parameters_handler.args(*task.args)
            kwargs = parameters_handler.kwargs(**task.kwargs)
        return ScheduledTask(
            executor=task.executor(
                proxy=partial_proxy,
                target=function_handler,
                name=task.name,
                args=args,
                kwargs=kwargs,
            ),
            name=task.name,
            target=task.target,
            args=task.args,
            kwargs=task.kwargs,
            dependencies=task.dependencies,
            priority=task.priority,
            processes=task.processes,
            threads=task.threads,
            continual=task.continual,
            initialized=True,
        )

    def enough_workers(self, task: ScheduledTask) -> bool:
        return bool(
            task.executor.__base__ == Process and
            task.processes < self.processes
        ) or bool(
            task.executor.__base__ == Thread and
            task.processes < self.processes and
            task.threads < self.threads
        )

    def available_worker(self, task: ScheduledTask) -> bool:
        return bool(
            task.executor.__base__ == Process and
            self.active_processes + task.processes < self.processes
        ) or bool(
            task.executor.__base__ == Thread and
            self.active_processes + task.processes < self.processes and
            self.active_threads + task.threads < self.threads
        )
