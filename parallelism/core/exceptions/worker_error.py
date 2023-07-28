from __future__ import annotations

__all__ = ('WorkerError',)


class WorkerError(Exception):
    def __init__(self, message: str, processes: int, threads: int) -> None:
        super().__init__(message, processes, threads)
        self.message = message
        self.processes = processes
        self.threads = threads
