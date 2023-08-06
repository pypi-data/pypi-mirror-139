import os
import logging


def _add_handler(logger: logging.Logger, formatter: logging.Formatter, handler: logging.Handler):
    handler.setFormatter(formatter)
    logger.addHandler(handler)


LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
ENABLE_STREAM = os.getenv('LOG_TO_STREAM', 'true')
logger = logging.getLogger('hestia_earth.orchestrator')
logger.setLevel(logging.getLevelName('DEBUG'))

# stream logging
_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(message)s')

if ENABLE_STREAM == 'true':
    handler = logging.StreamHandler()
    handler.setLevel(logging.getLevelName(LOG_LEVEL))
    _add_handler(logger, _formatter, handler)


def log_to_file(filepath: str):
    """
    By default, all logs are saved into a file with path stored in the env variable `LOG_FILENAME`.
    If you do not set the environment variable `LOG_FILENAME`, you can use this function with the file path.

    Parameters
    ----------
    filepath : str
        Path of the file.
    """
    formatter = logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", '
        '"filename": "%(filename)s", "message": "%(message)s"}',
        '%Y-%m-%dT%H:%M:%S%z')
    handler = logging.FileHandler(filepath, encoding='utf-8')
    handler.setLevel(logging.getLevelName('DEBUG'))
    _add_handler(logger, formatter, handler)


LOG_FILENAME = os.getenv('LOG_FILENAME')
if LOG_FILENAME is not None:
    log_to_file(LOG_FILENAME)
