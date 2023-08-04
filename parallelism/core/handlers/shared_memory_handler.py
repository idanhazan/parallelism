from __future__ import annotations

from typing import TYPE_CHECKING
from parallelism.core.scheduled_task import ScheduledTask

if TYPE_CHECKING:
    from multiprocessing.managers import DictProxy
    from typing import Dict, List, Tuple

__all__ = ('SharedMemoryHandler',)


class SharedMemoryHandler:
    __slots__ = (
        'tasks',
        'proxy',
        'execution_time',
        'elapsed_time',
        'raise_exception',
        'return_value',
        'prerequisites',
    )

    def __init__(
        self,
        tasks: List[ScheduledTask],
        proxy: DictProxy,
        prerequisites: Dict[str, Tuple[ScheduledTask, ...]],
    ) -> None:
        self.tasks = tasks
        self.proxy = proxy
        self.prerequisites = prerequisites
        self.execution_time = {}
        self.elapsed_time = {}
        self.raise_exception = {}
        self.return_value = {}

    def free(self, index: int, task: ScheduledTask) -> None:
        proxy = self.proxy.get(task.name)
        if (
            proxy.get('finish') and
            self.has_shared_memory(task) and
            self.prerequisites_been_initialized(task)
        ):
            self.execution_time[task.name] = proxy.get('execution_time')
            if proxy.get('elapsed_time'):
                self.elapsed_time[task.name] = proxy.get('elapsed_time')
            if proxy.get('raise_exception'):
                self.raise_exception[task.name] = proxy.get('raise_exception')
            elif task.continual:
                self.return_value[task.name] = proxy.get('return_value')
            self.tasks[index] = ScheduledTask(
                executor=task.executor.__class__.__base__,
                name=task.name,
                target=task.target,
                args=(),
                kwargs={},
                dependencies=task.dependencies,
                priority=task.priority,
                processes=task.processes,
                threads=task.threads,
                continual=task.continual,
                initialized=task.initialized,
            )
            del self.proxy[task.name]['execution_time']
            del self.proxy[task.name]['elapsed_time']
            del self.proxy[task.name]['raise_exception']
            del self.proxy[task.name]['return_value']

    def has_shared_memory(self, task: ScheduledTask) -> bool:
        proxy = self.proxy.get(task.name)
        return (
            'execution_time' in proxy or
            'elapsed_time' in proxy or
            'raise_exception' in proxy or
            'return_value' in proxy
        )

    def prerequisites_been_initialized(self, task: ScheduledTask) -> bool:
        task_prerequisites = self.prerequisites.get(task.name)
        tasks = tuple(task for task in task_prerequisites)
        return all(
            task.initialized for task in self.tasks
            if task in tasks
        )

    def sort(self):
        self.execution_time = dict(
            sorted(
                self.execution_time.items(),
                key=lambda item: item[1],
            ),
        )
        self.elapsed_time = dict(
            sorted(
                self.elapsed_time.items(),
                key=lambda item: self.execution_time.get(item[0]),
            ),
        )
        self.raise_exception = dict(
            sorted(
                self.raise_exception.items(),
                key=lambda item: self.execution_time.get(item[0]),
            ),
        )
        self.return_value = dict(
            sorted(
                self.return_value.items(),
                key=lambda item: self.execution_time.get(item[0]),
            ),
        )
