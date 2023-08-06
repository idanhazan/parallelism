from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from multiprocessing.managers import DictProxy
    from typing import List, Tuple

    from parallelism.core.scheduled_task import ScheduledTask

__all__ = ('ResourceHandler',)


class ResourceHandler:
    __slots__ = (
        'tasks',
        'proxy',
        'system_processor',
        'system_memory',
        'graphics_processor',
        'graphics_memory',
    )

    def __init__(
        self,
        tasks: List[ScheduledTask],
        proxy: DictProxy,
        system_processor: float,
        system_memory: float,
        graphics_processor: float,
        graphics_memory: float,
    ) -> None:
        self.tasks = tasks
        self.proxy = proxy
        self.system_processor = system_processor
        self.system_memory = system_memory
        self.graphics_processor = graphics_processor
        self.graphics_memory = graphics_memory

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
    def system_processor_usage(self) -> float:
        return sum(task.system_processor for task in self.active_tasks)

    @property
    def system_memory_usage(self) -> float:
        return sum(task.system_memory for task in self.active_tasks)

    @property
    def graphics_processor_usage(self) -> float:
        return sum(task.graphics_processor for task in self.active_tasks)

    @property
    def graphics_memory_usage(self) -> float:
        return sum(task.graphics_memory for task in self.active_tasks)

    def enough_resources(self, task: ScheduledTask) -> bool:
        sp = self.system_processor - self.system_processor_usage
        sm = self.system_memory - self.system_memory_usage
        gp = self.graphics_processor - self.graphics_processor_usage
        gm = self.graphics_memory - self.graphics_memory_usage
        return bool(
            task.system_processor <= sp and
            task.system_memory <= sm and
            task.graphics_processor <= gp and
            task.graphics_memory <= gm
        )
