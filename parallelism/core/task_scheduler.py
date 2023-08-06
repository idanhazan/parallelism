from __future__ import annotations

from multiprocessing import Manager, Process
from threading import Thread
from typing import TYPE_CHECKING

from parallelism.core.handlers.dependency_handler import DependencyHandler
from parallelism.core.handlers.function_handler import FunctionHandler
from parallelism.core.handlers.parameters_handler import ParametersHandler
from parallelism.core.handlers.resource_handler import ResourceHandler
from parallelism.core.handlers.shared_memory_handler import SharedMemoryHandler
from parallelism.core.handlers.worker_handler import WorkerHandler
from parallelism.core.scheduled_task import ScheduledTask
from parallelism.core.scheduler_result import SchedulerResult

if TYPE_CHECKING:
    from typing import Literal, Tuple, Union

__all__ = ('TaskScheduler',)


class TaskScheduler:
    __slots__ = (
        'tasks',
        'returns',
        'processes',
        'threads',
        'system_processor',
        'system_memory',
        'graphics_processor',
        'graphics_memory',
        'manager',
        'proxy',
        'worker_handler',
        'resource_handler',
        'dependency_handler',
        'shared_memory_handler',
    )

    def __init__(
        self,
        tasks: Tuple[ScheduledTask, ...],
        processes: int,
        threads: int,
        system_processor: Union[int, float],
        system_memory: Union[int, float],
        graphics_processor: Union[int, float],
        graphics_memory: Union[int, float],
    ) -> None:
        self.tasks = sorted(tasks, key=lambda task: task.priority)
        self.processes = processes
        self.threads = threads
        self.system_processor = system_processor
        self.system_memory = system_memory
        self.graphics_processor = graphics_processor
        self.graphics_memory = graphics_memory
        self.manager = None
        self.proxy = None
        self.worker_handler = None
        self.resource_handler = None
        self.dependency_handler = None
        self.shared_memory_handler = None

    @property
    def finished(self) -> bool:
        return all(
            task.initialized and
            self.proxy.get(task.name).get('finish')
            for task in self.tasks
        )

    def execute(self) -> SchedulerResult:
        self.manager = Manager()
        self.proxy = self.manager.dict()
        self.worker_handler = WorkerHandler(
            tasks=self.tasks,
            proxy=self.proxy,
            processes=self.processes,
            threads=self.threads,
        )
        self.resource_handler = ResourceHandler(
            tasks=self.tasks,
            proxy=self.proxy,
            system_processor=self.system_processor,
            system_memory=self.system_memory,
            graphics_processor=self.graphics_processor,
            graphics_memory=self.graphics_memory,
        )
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
            if not self.worker_handler.enough_workers(task):
                self.proxy[task.name] = self.manager.dict()
                task = self.initialize(task, blocked='worker')
                self.tasks[index] = task
            if not self.resource_handler.enough_resources(task):
                self.proxy[task.name] = self.manager.dict()
                task = self.initialize(task, blocked='resource')
                self.tasks[index] = task
        while not self.finished:
            for index, task in enumerate(self.tasks):
                if task.initialized:
                    self.shared_memory_handler.free(index, task)
                    continue
                if not self.resource_handler.enough_resources(task):
                    continue
                if not self.worker_handler.available_worker(task):
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
        for index, task in enumerate(self.tasks):
            self.shared_memory_handler.free(index, task)
        self.manager.shutdown()
        self.shared_memory_handler.sort()
        return SchedulerResult(
            self.shared_memory_handler.execution_time,
            self.shared_memory_handler.elapsed_time,
            self.shared_memory_handler.raise_exception,
            self.shared_memory_handler.return_value,
        )

    def initialize(
        self,
        task: ScheduledTask,
        blocked: Literal['dependency', 'resource', 'worker'] = None,
    ) -> ScheduledTask:
        full_proxy = self.proxy
        partial_proxy = self.proxy.get(task.name)
        blocker = None
        if blocked == 'dependency':
            tasks = self.dependency_handler.blocking_tasks(task)
            blocker = {'reason': blocked, 'tasks': tasks}
        if blocked == 'resource':
            sp = abs(min(0, self.system_processor - task.system_processor))
            sm = abs(min(0, self.system_memory - task.system_memory))
            gp = abs(min(0, self.graphics_processor - task.graphics_processor))
            gm = abs(min(0, self.graphics_memory - task.graphics_memory))
            blocker = {
                'reason': blocked,
                'system_processor': sp,
                'system_memory': sm,
                'graphics_processor': gp,
                'graphics_memory': gm,
            }
        if blocked == 'worker':
            processes = 0
            threads = 0
            if task.executor.__base__ == Process:
                processes = abs(min(0, self.processes - (task.processes + 1)))
                threads = abs(min(0, self.threads))
            if task.executor.__base__ == Thread:
                processes = abs(min(0, self.processes - task.processes))
                threads = abs(min(0, self.threads - (task.threads + 1)))
            blocker = {
                'reason': blocked,
                'processes': processes,
                'threads': threads,
            }
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
            system_processor=task.system_processor,
            system_memory=task.system_memory,
            graphics_processor=task.graphics_processor,
            graphics_memory=task.graphics_memory,
            continual=task.continual,
            initialized=True,
        )
