from __future__ import annotations

from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

__all__ = ('RaiseException',)


class RaiseException(NamedTuple):
    exception: Exception
    traceback: Optional[str] = None

    def __repr__(self) -> str:
        return repr(self.exception)
