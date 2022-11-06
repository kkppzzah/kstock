# -*- coding:utf-8 -*-
import sys
from typing import Tuple

import numba
import numpy as np

from kstock.ta.indicator.ema import ema


# @numba.jit(nopython=True, cache=True)
def macd(
        closes: np.ndarray, slow_period: int = 26, fast_period: int = 12,
        signalperiod: int = 9
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
        DIF=EMA_(close,12)-EMA(close,26)
        DEM=EMA(DIF,9)
        OSC=DIF-DEM=DIF-MACD
    :param signalperiod:
    :param closes:
    :param slow_period:
    :param fast_period:
    :return:
    """
    dif = ema(closes, fast_period) - ema(closes, slow_period)
    dem = ema(dif, signalperiod)
    osc = dif - dem
    return dif, dem, osc * 2


if 'pytest' not in sys.modules:
    macd = numba.jit(macd, nopython=True, cache=True)
