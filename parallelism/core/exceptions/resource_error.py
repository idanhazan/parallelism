from __future__ import annotations

from typing import Union

__all__ = ('ResourceError',)


class ResourceError(Exception):
    def __init__(
        self,
        message: str,
        system_processor: Union[int, float],
        system_memory: Union[int, float],
        graphics_processor: Union[int, float],
        graphics_memory: Union[int, float],
    ) -> None:
        super().__init__(
            message,
            system_processor,
            system_memory,
            graphics_processor,
            graphics_memory,
        )
        self.message = message
        self.system_processor = system_processor
        self.system_memory = system_memory
        self.graphics_processor = graphics_processor
        self.graphics_memory = graphics_memory
