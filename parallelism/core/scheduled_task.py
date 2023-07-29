from __future__ import annotations

from typing import NamedTuple, TYPE_CHECKING

from parallelism.core.executors.process_executor import ProcessExecutor
from parallelism.core.executors.thread_executor import ThreadExecutor
from parallelism.core.return_value import ReturnValue

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Tuple, Type, Union

__all__ = ('ScheduledTask',)


class ScheduledTask(NamedTuple):
    executor: Union[
        ProcessExecutor,
        ThreadExecutor,
        Type[ProcessExecutor],
        Type[ThreadExecutor],
    ]
    name: str
    target: Callable[..., Any]
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
    dependencies: Tuple[ScheduledTask, ...]
    priority: Union[int, float]
    processes: int
    threads: int
    continual: bool
    initialized: bool

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: ScheduledTask) -> bool:
        return type(self) is type(other) and self.name == other.name

    def __repr__(self) -> str:
        parameters = (
            'executor={!r}'.format(self.reformat_executor),
            'name={!r}'.format(self.name),
            'target={!r}'.format(self.reformat_target),
            'args={!r}'.format(self.amount_of_args),
            'kwargs={!r}'.format(self.amount_of_kwargs),
            'dependencies={!r}'.format(self.amount_of_dependencies),
            'priority={!r}'.format(self.priority),
            'processes={!r}'.format(self.processes),
            'threads={!r}'.format(self.threads),
            'continual={!r}'.format(self.continual),
        )
        parameters = ', '.join(parameters)
        return f'{self.__class__.__name__}({parameters})'

    @property
    def reformat_executor(self) -> str:
        executor = self.executor
        if isinstance(self.executor, (ProcessExecutor, ThreadExecutor)):
            executor = executor.__class__
        return executor.__base__.__name__

    @property
    def reformat_target(self) -> str:
        target = self.target
        module = getattr(target, '__module__')
        qualified_name = getattr(target, '__qualname__', repr(target))
        return f'{module}.{qualified_name}'

    @property
    def amount_of_args(self) -> int:
        return len(self.args)

    @property
    def amount_of_kwargs(self) -> int:
        return len(self.kwargs)

    @property
    def amount_of_dependencies(self) -> int:
        return len(self.dependencies)

    @property
    def depends_on_dependencies(self) -> Tuple[ScheduledTask, ...]:
        return tuple(task for task in self.dependencies)
        # return tuple(task.name for task in self.dependencies)

    @property
    def depends_on_parameters(self) -> Tuple[ScheduledTask, ...]:
        tasks = {}
        for parameter in list(self.args) + list(self.kwargs.values()):
            if isinstance(parameter, ReturnValue):
                task = getattr(parameter, ':task')
                if task not in tasks:
                    tasks[task] = None
        return tuple(tasks.keys())

    @property
    def return_value(self) -> ReturnValue:
        return ReturnValue(task=self)
