# -*- coding:utf-8 -*-

class EnvironmentVariableNotSetException(Exception):
    def __init__(self, argument: str):
        super(EnvironmentVariableNotSetException, self).__init__("Environment variable '%s' is not set" % argument)


class PeriodTypeNotSupportedException(Exception):
    def __init__(self, period: str):
        super(PeriodTypeNotSupportedException, self).__init__("Period type '%s' is not supported" % period)


class StockCodeNotSupportedException(Exception):
    def __init__(self, code: str):
        super(StockCodeNotSupportedException, self).__init__("Stock code '%s' is not supported" % code)
