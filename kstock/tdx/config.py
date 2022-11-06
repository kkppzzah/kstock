# -*- encoding:utf-8 -*-
import environ

from kstock.utils.decorators import singleton


@environ.config(prefix='TDX')
class TdxConfig:
    vipdoc = environ.var(name='TDX_VIPDOC', default='')
    root = environ.var(name='TDX_ROOT', default='')


@singleton
def instance() -> TdxConfig:
    return environ.to_config(TdxConfig)
