from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from parallelism.core.scheduled_task import ScheduledTask

__all__ = ('ReturnValue',)


class ReturnValue:
    __slots__ = ('task', 'transformations')

    def __init__(self, task: ScheduledTask) -> None:
        self.task = task
        self.transformations = []

    def __call__(self, *args: Any, **kwargs: Any) -> ReturnValue:
        transformations = getattr(self, ':transformations')
        transformations.append(('__call__', (args, kwargs)))
        return self

    def __getattribute__(self, name: str) -> ReturnValue:
        if name.startswith(':'):
            return object.__getattribute__(self, name[1:])
        transformations = getattr(self, ':transformations')
        transformations.append(('__getattribute__', name))
        return self

    def __getitem__(self, key: Any) -> ReturnValue:
        transformations = getattr(self, ':transformations')
        transformations.append(('__getitem__', key))
        return self

    def __repr__(self):
        class_name = getattr(self, ':__class__').__name__
        task = getattr(self, ':task')
        return f'{class_name}(task={task!r})'
