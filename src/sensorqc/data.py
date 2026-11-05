from __future__ import annotations

import json

import pandas as pd


def load_iv(path: str, param: str) -> pd.Series:
    """USGS NWIS instantaneous-value JSON -> series on a regular 5-minute grid (gaps stay NaN)."""
    d = json.load(open(path))  # noqa: SIM115
    for ts in d["value"]["timeSeries"]:
        if ts["variable"]["variableCode"][0]["value"] == param and ts["values"][0]["value"]:
            v = ts["values"][0]["value"]
            s = pd.Series(
                [float(x["value"]) for x in v],
                index=pd.to_datetime([x["dateTime"] for x in v], utc=True),
            )
            return s[~s.index.duplicated()].asfreq("5min")
    raise KeyError(param)
