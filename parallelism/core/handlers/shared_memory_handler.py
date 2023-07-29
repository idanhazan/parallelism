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
        'elapsed_time',
        'error_handler',
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
        self.elapsed_time = {}
        self.error_handler = {}
        self.return_value = {}

    def free(self, index: int, task: ScheduledTask) -> None:
        proxy = self.proxy.get(task.name)
        if (
            proxy.get('finish') and
            self.has_shared_memory(task) and
            self.prerequisites_been_initialized(task)
        ):
            if proxy.get('elapsed_time'):
                self.elapsed_time[task.name] = proxy.get('elapsed_time')
            if proxy.get('error_handler'):
                self.error_handler[task.name] = proxy.get('error_handler')
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
            del self.proxy[task.name]['elapsed_time']
            del self.proxy[task.name]['error_handler']
            del self.proxy[task.name]['return_value']

    def has_shared_memory(self, task: ScheduledTask) -> bool:
        proxy = self.proxy.get(task.name)
        return (
            'elapsed_time' in proxy or
            'error_handler' in proxy or
            'return_value' in proxy
        )

    def prerequisites_been_initialized(self, task: ScheduledTask) -> bool:
        task_prerequisites = self.prerequisites.get(task.name)
        tasks = tuple(task for task in task_prerequisites)
        return all(
            task.initialized for task in self.tasks
            if task in tasks
        )
