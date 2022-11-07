# -*- coding:utf-8 -*-

CANDLE_PERIOD_TYPE_D = 'd'  # 日K线周期
CANDLE_PERIOD_TYPE_MIN_1 = 'M1'  # 1分钟K线周期
CANDLE_PERIOD_TYPE_MIN_5 = 'M5'  # 5分钟K线周期

candle_period_type_tdx_file_map = {
    CANDLE_PERIOD_TYPE_D: {'path': 'lday', 'suffix': 'day'},
    CANDLE_PERIOD_TYPE_MIN_1: {'path': 'minline', 'suffix': 'lc1'},
    CANDLE_PERIOD_TYPE_MIN_5: {'path': 'fzline', 'suffix': 'lc5'}
}

stock_code_tdx_file_map = [
    {
        'prefix': '6', 'path': 'sh', 'filename_format': 'sh{code}.{suffix}'
    },
    {
        'prefix': '0', 'path': 'sz', 'filename_format': 'sz{code}.{suffix}'
    },
    {
        'prefix': '3', 'path': 'sz', 'filename_format': 'sz{code}.{suffix}'
    }
]

CANDLE_ITEM_LEN = 32  # 每个K线长度是32个字节。
