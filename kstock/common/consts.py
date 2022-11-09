# -*- coding:utf-8 -*-
from enum import Enum, auto


class AggregateTimeType(Enum):
    FIRST_DATA_TIME = auto()
    LAST_DATA_TIME = auto()
    PERIOD_START_TIME = auto()
    PERIOD_END_TIME = auto
