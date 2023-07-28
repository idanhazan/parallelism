import decimal
import logging

# decimal configuration
DECIMAL_PRECISION = 2
DECIMAL_ROUNDING_MODE = decimal.ROUND_HALF_UP

# logging configuration
LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = '{timestamp} {level} {logger} - {message}'.format(
    timestamp='%(asctime)s',
    level='[%(levelname)s]',
    logger='[%(name)s:%(process)d:%(thread)d]',
    message='%(message)s',
)
