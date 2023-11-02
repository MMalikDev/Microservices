import os
import sys
from logging import config, getLogger
from time import perf_counter
from typing import Any, Callable

# ---------------------------------------------------------------------- #
# ENV variables
# ---------------------------------------------------------------------- #
load_variable = os.getenv


def load_bool(key: str, default: bool = False) -> bool:
    env = load_variable(key, f"{default}").upper() in ["1", "TRUE"]
    args = key in sys.argv
    return env or args


LOG_LEVEL = load_variable("LOG_LEVEL", "INFO")
DISABLE_EXTRA_LOGS = not load_bool("THIRD_PARTY_LOGS", True)

# ---------------------------------------------------------------------- #
# Logging                                                                #
# ---------------------------------------------------------------------- #
logging_configs = {
    "version": 1,
    "disable_existing_loggers": DISABLE_EXTRA_LOGS,
    "formatters": {
        "simple": {"format": "[%(levelname)s] %(message)s"},
        "timed": {
            "format": "%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "simple",
            "level": LOG_LEVEL,
        },
    },
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": ["console"],
        }
    },
}

config.dictConfig(logging_configs)
logger = getLogger(f"{__name__}")


# ---------------------------------------------------------------------- #
# Function                                                               #
# ---------------------------------------------------------------------- #
def unpack(list: list, separator: str = "\n") -> str:
    return separator.join(map(str, list))


def format_perf_count(start: float, end: float) -> str:
    secondes = "s"
    time_s = end - start

    millisecond = "ms"
    time_ms = time_s * 1000

    slow = int(time_s)  # Checks if time rounds to 1 or more

    if slow:
        duration = time_s
        unit = secondes
    else:
        duration = time_ms
        unit = millisecond

    return f"{duration:.4f}{unit}"


# ---------------------------------------------------------------------- #
# Decorator                                                              #
# ---------------------------------------------------------------------- #
def debug(func: Callable) -> Any:
    def wrapper(*args, **kwargs) -> Any:
        try:
            logger.debug(f"Starting: {func.__name__}")

            start = perf_counter()
            result = func(*args, **kwargs)
            end = perf_counter()
            time = format_perf_count(start, end)

            logger.debug(f"Completed: {func.__name__} - {time}")
            return result

        except Exception as error:
            message = f"Failed: {func.__name__} | "
            message += f"{error.__class__.__name__} - "
            message += f"{error}"
            logger.error(message)

    return wrapper


def test_logger(func: Callable) -> None:
    PASSED_ICON = "\u2705"
    FAILED_ICON = "\u274C"

    def wrapper(*args, **kwargs):
        try:
            start = perf_counter()
            func(*args, **kwargs)
            end = perf_counter()
            time = format_perf_count(start, end)

            message = f"{PASSED_ICON} - Passed: {func.__name__} | {time}"
            logger.info(message)

        except AssertionError as error:
            message = f"{FAILED_ICON} - Failed: {func.__name__} | "
            message += f"[{error.__class__.__name__}] {error}"
            logger.info(message)

    return wrapper


# ---------------------------------------------------------------------- #
# Class                                                                  #
# ---------------------------------------------------------------------- #
class Dict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    """dot.notation access to dictionary attributes"""
