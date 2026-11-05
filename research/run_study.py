"""USGS Susquehanna River near Darlington, MD (01579550), 2022, 5-minute data: sensor QC detectors.

usage: python research/run_study.py <USGS iv JSON file for site 01579550 year 2022>
Real, approved (reviewed) data, parameters: water temperature (00010), specific conductance (00095), turbidity (63680).
First half of the year: threshold calibration. Second half: evaluation.
 (a) false-alarm rate on the unaltered real second half;
 (b) detection of INJECTED faults (synthetic perturbations of the real series): spike, step, drift, flatline; fault size is expressed in units of the typical one-day change.
There are no real fault labels in these approved data. Injected-fault results are a labelled test, not field evidence.
"""

import json
import sys
from pathlib import Path

import numpy as np

from sensorqc.data import load_iv
from sensorqc.detectors import SCORES, threshold

POINT_RATE = 1e-3
N_FAULTS = 100
LEN = 12 * 12  # 12 hours of 5-minute points
MAGN = (
    1.0,
    3.0,
)  # fault size in units of the typical one-day change (robust MAD scale of x_t - x_{t-288})


def inject(x: np.ndarray, kind: str, start: int, mag: float, sd: float):
    y = x.copy()
    sl = slice(start, start + LEN)
    if kind == "spike":
        sl = slice(start, start + 1)
        y[sl] = y[sl] + mag * sd
    elif kind == "step":
        y[sl] = y[sl] + mag * sd
    elif kind == "drift":
        y[sl] = y[sl] + np.linspace(0, mag * sd, LEN)
        y[start + LEN : start + 2 * LEN] += mag * sd  # offset persists after the ramp
        sl = slice(start, start + LEN)
    elif kind == "flatline":
        y[sl] = y[start]
    return y, sl


def main(path: str):
    import pandas as pd

    out = {
        "note": "real approved USGS data (2022) + INJECTED synthetic faults; thresholds at a point exceedance "
        f"rate of {POINT_RATE} on the first half",
        "parameters": {},
    }
    rng = np.random.default_rng(0)
    for pname, code in (
        ("temperature", "00010"),
        ("specific_conductance", "00095"),
        ("turbidity", "63680"),
    ):
        s = load_iv(path, code)
        half = len(s) // 2
        cal, tst = s.iloc[:half], s.iloc[half:]
        d1 = tst.to_numpy()[288:] - tst.to_numpy()[:-288]
        sd = float(1.4826 * np.nanmedian(np.abs(d1 - np.nanmedian(d1))))
        thr = {k: threshold(f(cal), POINT_RATE) for k, f in SCORES.items()}
        res = {
            "n_cal": int(cal.notna().sum()),
            "n_test": int(tst.notna().sum()),
            "sd": sd,
            "thresholds": thr,
            "false_alarm_points_per_1000": {},
            "detection": {},
        }
        for k, f in SCORES.items():
            sc = f(tst)
            ok = ~np.isnan(sc)
            res["false_alarm_points_per_1000"][k] = float(1000 * (sc[ok] > thr[k]).mean())
        x = tst.to_numpy()
        for kind in ("spike", "step", "drift", "flatline"):
            for mag in MAGN:
                if kind == "flatline" and mag != MAGN[0]:
                    continue
                hits = {k: 0 for k in SCORES}
                n = 0
                starts = rng.integers(24 * 12, len(x) - 3 * LEN, N_FAULTS * 3)
                for st in starts:
                    if n >= N_FAULTS:
                        break
                    if np.isnan(x[st : st + 2 * LEN]).any():
                        continue
                    y, sl = inject(x, kind, int(st), mag, sd)
                    ys = pd.Series(y, index=tst.index)
                    for k, f in SCORES.items():
                        sc = f(ys)[sl]
                        hits[k] += int(np.nanmax(sc) > thr[k]) if np.isfinite(np.nanmax(sc)) else 0
                    n += 1
                key = kind if kind == "flatline" else f"{kind}_{mag:g}x"
                res["detection"][key] = {"n": n, **{k: hits[k] / max(n, 1) for k in SCORES}}
        out["parameters"][pname] = res
        print(pname, {k: round(v, 2) for k, v in res["false_alarm_points_per_1000"].items()})
        for key, v in res["detection"].items():
            print("  ", key, {k: round(x_, 2) for k, x_ in v.items() if k != "n"})
    Path(__file__).with_name("results.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
