# -*- coding:utf-8 -*-
import os
import importlib

import pytest

import kstock
from kstock.tdx.config import TdxConfig


@pytest.mark.parametrize(
    "tdx_vipdoc", [
        '',
        'D:\\海王星金融终端-中国银河证券\\vipdoc'
    ]
)
def test_tdx_config_instance(tdx_vipdoc: str) -> None:
    os.environ['TDX_VIPDOC'] = tdx_vipdoc
    importlib.reload(kstock.tdx.config)
    from kstock.tdx.config import instance
    config: TdxConfig = instance()
    assert config is not None
    assert config.vipdoc == tdx_vipdoc
