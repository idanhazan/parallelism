from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple

__all__ = ('DependencyError',)


class DependencyError(Exception):
    def __init__(self, message: str, tasks: Tuple[str, ...]) -> None:
        super().__init__(message, tasks)
        self.message = message
        self.tasks = tasks
