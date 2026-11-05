# Software Requirements Specification – SensorQC

- SR-1 `data.load_iv`: USGS instantaneous-value JSON to a 5-minute series.
- SR-2 `detectors`: scores `rate` (|first difference|), `residual_2h` (|x - median of previous 2 h|), `long_1d` (|x - median of previous day|), `flatline` (current run of identical values). All use past values only (a unit test checks this).
- SR-3 `detectors.threshold`: empirical (1 - 0.001) quantile of the scores on the calibration half (first half of 2022).
- SR-4 `research/run_study.py`: false-alarm points per 1000 on the unaltered second half; for each fault type, 100 injected faults of 12 hours (spike: one point) at sizes of 1x and 3x the typical one-day change (robust MAD scale of x_t - x_{t-288}); an injected fault is detected if any point in its window exceeds the threshold.
- SR-5 Three unit tests.
