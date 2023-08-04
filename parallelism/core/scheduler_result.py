from __future__ import annotations

from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime
    from typing import Any, Dict

    from parallelism.core.raise_exception import RaiseException

__all__ = ('SchedulerResult',)


class SchedulerResult(NamedTuple):
    execution_time: Dict[str, datetime]
    elapsed_time: Dict[str, float]
    raise_exception: Dict[str, RaiseException]
    return_value: Dict[str, Any]
