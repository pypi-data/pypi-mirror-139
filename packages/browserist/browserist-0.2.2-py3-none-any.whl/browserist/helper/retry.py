import time
from typing import Callable, List
from ..constant import interval, timeout

def get_text_from_element(func: Callable[[object, str], str], timeout: int = timeout.DEFAULT, wait_interval_seconds: float = interval.DEFAULT) -> str:
    text = str(func)
    i = 0
    retries = timeout / wait_interval_seconds
    while not text and i < retries:
        time.sleep(wait_interval_seconds)
        text = str(func)
        i += 1
    return text

def until_condition_is_true(func: Callable[[object, str | List[object]], bool], timeout: int = timeout.DEFAULT, wait_interval_seconds: float = interval.DEFAULT) -> None:
    i = 0
    retries = timeout / wait_interval_seconds
    while func is False and i < retries:
        time.sleep(wait_interval_seconds)
        i += 1
        # TODO: Raise exception if it times out/runs out of retries.

def until_condition_is_false(func: Callable[[object, str | List[object]], bool], timeout: int = timeout.DEFAULT, wait_interval_seconds: float = interval.DEFAULT) -> None:
    i = 0
    retries = timeout / wait_interval_seconds
    while func is True and i < retries:
        time.sleep(wait_interval_seconds)
        i += 1
        # TODO: Raise exception if it times out/runs out of retries.
