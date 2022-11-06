# -*- coding:utf-8 -*-
import os.path

from kstock.common.exception import (
    EnvironmentVariableNotSetException, PeriodTypeNotSupportedException, StockCodeNotSupportedException
)
from kstock.tdx import config
from kstock.tdx import consts


def vipdoc_root(root: str = '') -> str:
    return root if root else config.instance().vipdoc


def stock_candle_file_path(code: str, period: str, vipdoc_root_path: str = '') -> str:
    vipdoc_root_path = vipdoc_root(vipdoc_root_path)
    if not vipdoc_root_path:
        raise EnvironmentVariableNotSetException('TDX_VIPDOC')
    code_file_config_candidate = None
    for code_file_config in consts.stock_code_tdx_file_map:
        if code.startswith(code_file_config['prefix']):
            code_file_config_candidate = code_file_config
            break
    if not code_file_config_candidate:
        raise StockCodeNotSupportedException(code)
    period_type_file_config = consts.candle_period_type_tdx_file_map.get(period)
    if not period_type_file_config:
        raise PeriodTypeNotSupportedException(period)
    return os.path.join(
        vipdoc_root_path,
        code_file_config_candidate['path'],
        period_type_file_config['path'],
        code_file_config_candidate['filename_format'].format(code=code, suffix=period_type_file_config['suffix'])
    )


def tdx_root(root: str = '') -> str:
    return root if root else config.instance().root


def block_file_dir(tdx_root_path: str = '') -> str:
    tdx_root_path = tdx_root(tdx_root_path)
    if not tdx_root_path:
        raise EnvironmentVariableNotSetException('TDX_ROOT')
    return os.path.join(
        tdx_root_path,
        'T0002',
        'blocknew'
    )


def is_stock_market_sh(code: str) -> bool:
    return code.startswith('6')
