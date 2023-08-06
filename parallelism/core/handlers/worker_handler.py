from __future__ import annotations

from multiprocessing import Process
from threading import Thread
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from multiprocessing.managers import DictProxy
    from typing import List, Tuple

    from parallelism.core.scheduled_task import ScheduledTask

__all__ = ('WorkerHandler',)


class WorkerHandler:
    __slots__ = ('tasks', 'proxy', 'processes', 'threads')

    def __init__(
        self,
        tasks: List[ScheduledTask],
        proxy: DictProxy,
        processes: int,
        threads: int,
    ) -> None:
        self.tasks = tasks
        self.proxy = proxy
        self.processes = processes
        self.threads = threads

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
