# -*- coding:utf-8 -*-
import random
import string

from kstock.utils.decorators import singleton


def test_singleton() -> None:
    value = ''.join(random.choices(string.ascii_letters, k=20))

    @singleton
    def singleton_creator():
        return str(value)

    instance1: str = singleton_creator()
    instance2: str = singleton_creator()

    assert instance1 is not None and isinstance(instance1, str)
    assert instance1 == value

    assert id(instance1) == id(instance2)
    assert instance2 == value
