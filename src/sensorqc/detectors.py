from __future__ import annotations

import numpy as np
import pandas as pd

WIN = 24  # 2 hours of 5-minute points
LONG = 12 * 24  # 1 day


def mad_scale(x: np.ndarray) -> float:
    x = x[~np.isnan(x)]
    return float(1.4826 * np.median(np.abs(x - np.median(x))) + 1e-9)


def score_rate(x: pd.Series) -> np.ndarray:
    """|first difference|; large for spikes and jumps."""
    return np.abs(x.diff()).to_numpy()


def score_residual(x: pd.Series) -> np.ndarray:
    """|x - median of the previous 2 hours| (past only)."""
    med = x.shift(1).rolling(WIN, min_periods=WIN // 2).median()
    return np.abs(x - med).to_numpy()


def score_long(x: pd.Series) -> np.ndarray:
    """|x - median of the previous day|; sensitive to steps and drifts, but also to real events."""
    med = x.shift(1).rolling(LONG, min_periods=LONG // 2).median()
    return np.abs(x - med).to_numpy()


def score_flat(x: pd.Series) -> np.ndarray:
    """Length of the current run of identical consecutive values."""
    same = (x.diff() == 0).to_numpy()
    out = np.zeros(len(x))
    run = 0
    for i, s in enumerate(same):
        run = run + 1 if s else 0
        out[i] = run
    return out


SCORES = {
    "rate": score_rate,
    "residual_2h": score_residual,
    "long_1d": score_long,
    "flatline": score_flat,
}


def threshold(scores: np.ndarray, rate: float) -> float:
    """Point-level exceedance threshold: the (1 - rate) empirical quantile of calibration scores."""
    s = scores[~np.isnan(scores)]
    return float(np.quantile(s, 1 - rate))
