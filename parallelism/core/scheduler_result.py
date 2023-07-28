from __future__ import annotations

from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict

    from parallelism.core.handlers.error_handler import ErrorHandler

__all__ = ('SchedulerResult',)


class SchedulerResult(NamedTuple):
    elapsed_time: Dict[str, float]
    error_handler: Dict[str, ErrorHandler]
    return_value: Dict[str, Any]
