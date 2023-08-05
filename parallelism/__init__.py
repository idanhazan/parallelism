from parallelism.api_reference import *
from parallelism.config import LOGGING_LEVEL, LOGGING_FORMAT
from parallelism.logger import initialize_logger

__all__ = ('scheduled_task', 'task_scheduler')
__version__ = (0, 1, 1)

initialize_logger(formatter=LOGGING_FORMAT, level=LOGGING_LEVEL)
