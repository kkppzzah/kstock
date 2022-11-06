# -*- coding:utf-8 -*-
from typing import Dict

import numpy as np
import pytest

from kstock.ta.indicator.macd import macd


@pytest.mark.parametrize(
    "close_set, macd_set", [
        [
            np.array([20.94, 20.30, 20.55, 20.33, 20.33], dtype=np.float64),
            {
                'dif': np.array([0.00, -0.05, -0.07, -0.10, -0.13], dtype=np.float64),
                'dem': np.array([0.00, -0.01, -0.02, -0.04, -0.06], dtype=np.float64),
                'osc': np.array([0.00, -0.08, -0.10, -0.13, -0.14], dtype=np.float64)
            }
        ],
    ]
)
def test_macd(close_set: np.ndarray, macd_set: Dict) -> None:
    dif, dem, osc = macd(close_set)
    assert np.array_equal(macd_set['dif'], np.around(dif, 2))
    assert np.array_equal(macd_set['dem'], np.around(dem, 2))
    assert np.array_equal(macd_set['osc'], np.around(osc, 2))
