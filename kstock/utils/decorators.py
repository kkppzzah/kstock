# -*- utf-8 -*-
import functools
from typing import Callable, Any


def singleton(creator: Callable) -> Callable:
    class Singleton(object):
        def __init__(self):
            self._instance = None

        @property
        def instance(self) -> Any:
            return self._instance

        @instance.setter
        def instance(self, instance: Any):
            self._instance = instance

    _singleton = Singleton()

    @functools.wraps(creator)
    def wrapper(*args, **kwargs) -> Any:
        if _singleton.instance is None:
            _singleton.instance = creator(*args, **kwargs)
        return _singleton.instance

    return wrapper
