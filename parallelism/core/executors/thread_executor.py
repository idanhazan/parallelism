from __future__ import annotations

from threading import Thread
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from multiprocessing.managers import DictProxy
    from typing import Any

__all__ = ('ThreadExecutor',)


class ThreadExecutor(Thread):
    def __init__(self, proxy: DictProxy, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        proxy['run'] = False
        proxy['start'] = False
        proxy['join'] = False
        proxy['terminate'] = None
        proxy['kill'] = None
        proxy['close'] = None
        self.proxy = proxy

    def run(self) -> None:
        self.proxy['run'] = True
        super().run()

    def start(self) -> None:
        self.proxy['start'] = True
        super().start()

    def join(self, timeout: float = None) -> None:
        self.proxy['join'] = True
        super().join(timeout)
