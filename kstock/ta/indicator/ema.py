# -*- coding:utf-8 -*-
import sys

import numba
import numpy as np


# @numba.jit(nopython=True, cache=True)
def ema(data: np.ndarray, period: int) -> np.ndarray:
    data_len = data.shape[0]
    ema_result: np.ndarray = np.zeros(data_len, dtype=np.dtype('f8'))
    w_factor_1, w_factor_2 = 2 / (period + 1), (period - 1) / (period + 1)
    for idx in range(data_len):
        if idx == 0:
            ema_result[idx] = data[idx]
        else:
            ema_result[idx] = w_factor_1 * data[idx] + w_factor_2 * ema_result[idx - 1]
    return ema_result


if 'pytest' not in sys.modules:
    ema = numba.jit(ema, nopython=True, cache=True)
