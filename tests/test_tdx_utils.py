# -*- coding:utf-8 -*-
import importlib
import os

import pytest

import kstock
import kstock.tdx.config
import kstock.tdx.utils
from kstock.common import exception


@pytest.mark.parametrize(
    "vipdoc_root, env_vipdoc, vipdoc_root_result", [
        ['', '', ''],
        [
            '',
            'D:\\海王星金融终端-中国银河证券\\vipdoc',
            'D:\\海王星金融终端-中国银河证券\\vipdoc'
        ],
        [
            'D:\\海王星金融终端-中国银河证券\\vipdoc1',
            'D:\\海王星金融终端-中国银河证券\\vipdoc',
            'D:\\海王星金融终端-中国银河证券\\vipdoc1'
        ],
    ]
)
def test_tdx_utils_vipdoc_root(vipdoc_root: str, env_vipdoc: str, vipdoc_root_result: str) -> None:
    os.environ['TDX_VIPDOC'] = env_vipdoc
    importlib.reload(kstock.tdx.config)
    importlib.reload(kstock.tdx.utils)
    from kstock.tdx import utils
    assert vipdoc_root_result == utils.vipdoc_root(vipdoc_root)


@pytest.mark.parametrize(
    "code, period, vipdoc_root, env_vipdoc, candle_file_path, exception_class", [
        [
            '',
            '',
            '',
            '',
            '',
            exception.EnvironmentVariableNotSetException
        ],
        [
            '700196',
            'd',
            '',
            'D:\\海王星金融终端-中国银河证券\\vipdoc',
            'D:\\海王星金融终端-中国银河证券\\vipdoc\\sh\\lday\\sh600196.day',
            exception.StockCodeNotSupportedException
        ],
        [
            '600196',
            'H1',
            '',
            'D:\\海王星金融终端-中国银河证券\\vipdoc',
            'D:\\海王星金融终端-中国银河证券\\vipdoc\\sh\\lday\\sh600196.day',
            exception.PeriodTypeNotSupportedException
        ],
        [
            '600196',
            'd',
            '',
            'D:\\海王星金融终端-中国银河证券\\vipdoc',
            'D:\\海王星金融终端-中国银河证券\\vipdoc\\sh\\lday\\sh600196.day',
            None
        ],
        [
            '600196',
            'M5',
            '',
            'D:\\海王星金融终端-中国银河证券\\vipdoc',
            'D:\\海王星金融终端-中国银河证券\\vipdoc\\sh\\fzline\\sh600196.lc5',
            None
        ],
        [
            '600196',
            'M1',
            '',
            'D:\\海王星金融终端-中国银河证券\\vipdoc',
            'D:\\海王星金融终端-中国银河证券\\vipdoc\\sh\\minline\\sh600196.lc1',
            None
        ],
    ]
)
def test_tdx_utils_stock_candle_file_path(
        code: str, period: str, vipdoc_root: str, env_vipdoc: str, candle_file_path: str, exception_class: type
):
    os.environ['TDX_VIPDOC'] = env_vipdoc
    importlib.reload(kstock.tdx.config)
    importlib.reload(kstock.tdx.utils)
    from kstock.tdx import utils
    if exception_class:
        with pytest.raises(exception_class):
            utils.stock_candle_file_path(code, period, vipdoc_root_path=vipdoc_root)
    else:
        assert candle_file_path == utils.stock_candle_file_path(code, period, vipdoc_root_path=vipdoc_root)


@pytest.mark.parametrize(
    "tdx_root, env_tdx_root, tdx_root_result", [
        ['', '', ''],
        [
            '',
            'D:\\海王星金融终端-中国银河证券',
            'D:\\海王星金融终端-中国银河证券'
        ],
        [
            'D:\\海王星金融终端-中国银河证券1',
            'D:\\海王星金融终端-中国银河证券',
            'D:\\海王星金融终端-中国银河证券1'
        ],
    ]
)
def test_tdx_utils_tdx_root(tdx_root: str, env_tdx_root: str, tdx_root_result: str) -> None:
    os.environ['TDX_ROOT'] = env_tdx_root
    importlib.reload(kstock.tdx.config)
    importlib.reload(kstock.tdx.utils)
    from kstock.tdx import utils
    assert tdx_root_result == utils.tdx_root(tdx_root)


@pytest.mark.parametrize(
    "tdx_root, env_tdx_root, block_file_dir_result, exception_class", [
        [
            '',
            '',
            '',
            exception.EnvironmentVariableNotSetException
        ],
        [
            '',
            'D:\\海王星金融终端-中国银河证券',
            'D:\\海王星金融终端-中国银河证券\\T0002\\blocknew',
            None
        ]
    ]
)
def test_tdx_utils_block_file_dir(
        tdx_root: str, env_tdx_root: str, block_file_dir_result: str, exception_class: type
):
    os.environ['TDX_ROOT'] = env_tdx_root
    importlib.reload(kstock.tdx.config)
    importlib.reload(kstock.tdx.utils)
    from kstock.tdx import utils
    if exception_class:
        with pytest.raises(exception_class) as exc_info:
            utils.block_file_dir(tdx_root_path=tdx_root)
        assert 'TDX_ROOT' in exc_info.value.args[0]
    else:
        assert block_file_dir_result == utils.block_file_dir(tdx_root_path=tdx_root)
