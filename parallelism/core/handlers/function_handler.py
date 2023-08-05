from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from time import time
from traceback import format_exc
from typing import TYPE_CHECKING

from parallelism.config import DECIMAL_PRECISION, DECIMAL_ROUNDING_MODE
from parallelism.core.exceptions.dependency_error import DependencyError
from parallelism.core.exceptions.worker_error import WorkerError
from parallelism.core.raise_exception import RaiseException
from parallelism.logger import get_logger

if TYPE_CHECKING:
    from multiprocessing.managers import DictProxy
    from typing import Any, Callable, Dict, Optional

__all__ = ('FunctionHandler',)


class FunctionHandler:
    __slots__ = ('name', 'target', 'proxy')

    def __init__(
        self,
        name: str,
        target: Callable[..., Any],
        proxy: DictProxy,
        blocker: Optional[Dict[str, Any]],
    ) -> None:
        self.name = name
        self.target = target
        self.proxy = proxy
        self.proxy['execution_time'] = datetime.now()
        self.proxy['elapsed_time'] = None
        self.proxy['raise_exception'] = None
        self.proxy['return_value'] = None
        self.proxy['finish'] = False
        self.proxy['complete'] = False
        if blocker:
            self.log_current_state(blocker)

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        start = time()
        try:
            self.proxy['return_value'] = self.target(*args, **kwargs)
            self.proxy['complete'] = True
        except Exception as exception:
            self.proxy['raise_exception'] = RaiseException(
                exception=exception,
                traceback=format_exc(),
            )
        finally:
            end = time()
            self.proxy['elapsed_time'] = end - start
            self.proxy['finish'] = True
            self.log_current_state()

    def log_current_state(
        self,
        blocker: Optional[Dict[str, Any]] = None,
    ) -> None:
        logger = get_logger()
        name = self.name
        elapsed_time = self.proxy.get('elapsed_time')
        elapsed_time = self.beautify_time(seconds=elapsed_time)
        raise_exception = self.proxy.get('raise_exception')
        if blocker and blocker.get('reason') == 'dependency':
            *left, right = blocker.get('tasks')
            pattern = '{!r} is being canceled, due to '
            if len(left) == 0:
                pattern += 'task {!r}'
                message = pattern.format(name, right)
            elif len(left) == 1:
                pattern += 'both tasks {} and {!r}'
                left = ', '.join(map(repr, left))
                message = pattern.format(name, left, right)
            else:
                pattern += 'tasks {}, and {!r}'
                left = ', '.join(map(repr, left))
                message = pattern.format(name, left, right)
            exception = DependencyError(
                message='{!r} has been canceled'.format(name),
                tasks=blocker.get('tasks'),
            )
            self.proxy['raise_exception'] = RaiseException(exception)
            self.proxy['finish'] = True
            logger.warning(msg=message)
        elif blocker and blocker.get('reason') == 'worker':
            processes = blocker.get('processes')
            threads = blocker.get('threads')
            pattern = '{!r} is being canceled, due to '
            if processes > 1 and threads > 1:
                pattern += 'lack of {!r} processes and also {!r} threads'
                message = pattern.format(name, processes, threads)
            elif processes > 1 and threads == 1:
                pattern += 'lack of {!r} processes and also {!r} thread'
                message = pattern.format(name, processes, threads)
            elif processes == 1 and threads > 1:
                pattern += 'lack of {!r} process and also {!r} threads'
                message = pattern.format(name, processes, threads)
            elif processes == 1 and threads == 1:
                pattern += 'lack of {!r} process and also {!r} thread'
                message = pattern.format(name, processes, threads)
            elif processes > 1 and threads == 0:
                pattern += 'lack of {!r} processes'
                message = pattern.format(name, processes)
            elif processes == 1 and threads == 0:
                pattern += 'lack of {!r} process'
                message = pattern.format(name, processes)
            elif processes == 0 and threads > 1:
                pattern += 'lack of {!r} threads'
                message = pattern.format(name, threads)
            elif processes == 0 and threads == 1:
                pattern += 'lack of {!r} thread'
                message = pattern.format(name, threads)
            else:
                pattern += 'lack of workers'
                message = pattern.format(name)
            exception = WorkerError(
                message='{!r} has been canceled'.format(name),
                processes=processes,
                threads=threads,
            )
            self.proxy['raise_exception'] = RaiseException(exception)
            self.proxy['finish'] = True
            logger.warning(msg=message)
        elif isinstance(raise_exception, RaiseException):
            pattern = '{!r} ran approximately {} - {!r}'
            message = pattern.format(name, elapsed_time, raise_exception)
            logger.error(msg=message)
        else:
            pattern = '{!r} ran approximately {}'
            message = pattern.format(name, elapsed_time)
            logger.info(msg=message)

    @staticmethod
    def beautify_time(
        seconds: float,
        decimals: int = DECIMAL_PRECISION,
        rounding: str = DECIMAL_ROUNDING_MODE,
    ) -> Optional[str]:
        if seconds is None:
            return None
        value = Decimal(value=seconds)
        zeroes = '0' * decimals
        exponent = Decimal(value=f'1.{zeroes}')
        if seconds < 1e-6:
            value *= Decimal(value=1e+9)
            unit = 'nanosecond'
        elif seconds < 1e-4:
            value *= Decimal(value=1e+6)
            unit = 'microsecond'
        elif seconds < 1:
            value *= Decimal(value=1e+4)
            unit = 'millisecond'
        elif seconds < 60:
            unit = 'second'
        elif seconds < 3600:
            value /= Decimal(value=60)
            unit = 'minute'
        elif seconds < 86400:
            value /= Decimal(value=3600)
            unit = 'hour'
        elif seconds < 604800:
            value /= Decimal(value=86400)
            unit = 'day'
        else:
            value /= Decimal(value=604800)
            unit = 'week'
        value = value.quantize(exp=exponent, rounding=rounding)
        if value != exponent:
            unit = f'{unit}s'
        value = str(value).rstrip('0').rstrip('.')
        return f'{value} {unit}'
