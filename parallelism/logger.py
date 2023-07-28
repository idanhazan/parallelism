from __future__ import annotations

from logging import getLogger, Formatter, StreamHandler

__all__ = ('get_logger', 'initialize_logger')


def get_logger():
    return getLogger(name='parallelism')


def initialize_logger(formatter: str, level: int) -> None:
    formatter = Formatter(fmt=formatter)
    stream_handler = StreamHandler()
    stream_handler.setFormatter(fmt=formatter)
    logger = get_logger()
    logger.setLevel(level=level)
    logger.addHandler(hdlr=stream_handler)
