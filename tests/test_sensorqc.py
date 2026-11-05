import numpy as np
import pandas as pd

from sensorqc.detectors import score_flat, score_rate, score_residual, threshold


def _s(n=500, seed=0):
    rng = np.random.default_rng(seed)
    return pd.Series(
        10 + rng.normal(0, 0.1, n), index=pd.date_range("2022-01-01", periods=n, freq="5min")
    )


def test_spike_gets_high_rate_and_residual_scores():
    s = _s()
    s.iloc[300] += 5
    assert np.nanargmax(score_rate(s)) in (300, 301)
    assert np.nanargmax(score_residual(s)) == 300


def test_flatline_run_length():
    s = _s()
    s.iloc[100:130] = s.iloc[100]
    f = score_flat(s)
    assert f[129] == 29 and f[50] == 0


def test_threshold_is_quantile_and_scores_use_only_past():
    sc = np.arange(1000.0)
    assert threshold(sc, 0.01) == np.quantile(sc, 0.99)
    s = _s()
    s2 = s.copy()
    s2.iloc[400] += 50
    assert np.array_equal(score_residual(s)[:400], score_residual(s2)[:400], equal_nan=True)
