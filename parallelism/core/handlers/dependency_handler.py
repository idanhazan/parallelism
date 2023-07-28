from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from multiprocessing.managers import DictProxy
    from typing import Dict, List, Literal, Set, Tuple

    from parallelism.core.scheduled_task import ScheduledTask

__all__ = ('DependencyHandler',)


class DependencyHandler:
    __slots__ = ('tasks', 'proxy', 'prerequisites')

    def __init__(self, tasks: List[ScheduledTask], proxy: DictProxy) -> None:
        self.tasks = tasks
        self.proxy = proxy
        self.prerequisites = self.tasks_prerequisites()

    def tasks_prerequisites(self) -> Dict[str, Tuple[ScheduledTask, ...]]:
        prerequisite = dict.fromkeys((task.name for task in self.tasks), ())
        for task in self.tasks:
            for dependent_task in task.depends_on_parameters:
                prerequisite[dependent_task.name] += (task,)
        return prerequisite

    def is_blocked(
        self,
        task: ScheduledTask,
        status: Literal['finish', 'complete'],
    ) -> bool:
        task_names = tuple(task.name for task in self.depends_on(task))
        return len(task_names) != sum(
            task.initialized and
            self.proxy.get(task.name).get(status)
            for task in self.tasks
            if task.name in task_names
        )

    def blocking_tasks(self, task: ScheduledTask) -> Tuple[str, ...]:
        task_names = tuple(task.name for task in self.depends_on(task))
        return tuple(
            task.name for task in self.tasks
            if (
                task.name in task_names and
                task.initialized and not
                self.proxy.get(task.name).get('complete')
            )
        )

    @staticmethod
    def depends_on(task: ScheduledTask) -> Set[ScheduledTask]:
        return set(task.depends_on_dependencies + task.depends_on_parameters)

    @classmethod
    def depth_first_search(
        cls,
        graph: Dict[ScheduledTask, Set[ScheduledTask]],
        node: ScheduledTask,
        visited: Dict[ScheduledTask, bool],
        stack: Dict[ScheduledTask, bool],
    ) -> bool:
        visited[node] = True
        stack[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                if cls.depth_first_search(graph, neighbor, visited, stack):
                    return True
            elif stack[neighbor]:
                return True
        stack[node] = False
        return False

    @classmethod
    def directed_acyclic_graph(cls, tasks: Tuple[ScheduledTask, ...]) -> bool:
        graph = {}
        for task in tasks:
            graph[task] = set()
        for task in tasks:
            dependencies = DependencyHandler.depends_on(task)
            for dependency in dependencies:
                if dependency not in graph:
                    return False
                graph[task].add(dependency)
        visited = {node: False for node in graph}
        stack = {node: False for node in graph}
        for node in graph:
            if not visited[node]:
                if cls.depth_first_search(graph, node, visited, stack):
                    return False
        return True
