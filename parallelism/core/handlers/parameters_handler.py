from __future__ import annotations

from typing import TYPE_CHECKING

from parallelism.core.return_value import ReturnValue

if TYPE_CHECKING:
    from multiprocessing.managers import DictProxy
    from typing import Any, Dict, Tuple

__all__ = ('ParametersHandler',)


class ParametersHandler:
    __slots__ = ('proxy',)

    def __init__(self, proxy: DictProxy) -> None:
        self.proxy = proxy

    def args(self, *args: Any) -> Tuple[Any, ...]:
        args = list(args)
        for index, value in enumerate(args):
            if isinstance(value, ReturnValue):
                task = getattr(value, ':task')
                transformations = getattr(value, ':transformations')
                value = self.proxy.get(task.name).get('return_value')
                for method, data in transformations:
                    if method == '__call__':
                        positionals, keywords = data
                        value = value(*positionals, **keywords)
                    if method == '__getattribute__':
                        value = getattr(value, data)
                    if method == '__getitem__':
                        value = value[data]
                args[index] = value
        return tuple(args)

    def kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs = dict(kwargs)
        for key, value in kwargs.items():
            if isinstance(value, ReturnValue):
                task = getattr(value, ':task')
                transformations = getattr(value, ':transformations')
                value = self.proxy.get(task.name).get('return_value')
                for method, data in transformations:
                    if method == '__call__':
                        positionals, keywords = data
                        value = value(*positionals, **keywords)
                    if method == '__getattribute__':
                        value = getattr(value, data)
                    if method == '__getitem__':
                        value = value[data]
                kwargs[key] = value
        return dict(kwargs)
