# articles-SensorQC

Automated quality-control tests for water-quality sensor streams (rate of change, residual to a short rolling median,
residual to a one-day median, flatline) evaluated on **real approved USGS 5-minute data** (Susquehanna River near
Darlington, MD, 2022: temperature, specific conductance, turbidity). The approved data carry **no fault labels**, so detection is
measured on **injected synthetic faults** (spike, step, drift, flatline) — a labelled test, not field evidence. TRL 4.

```
pip install -e ".[dev]" && python -m pytest
# data: USGS NWIS instantaneous values for site 01579550, 2022, parameters 00010,00095,63680 (JSON; not committed)
python research/run_study.py <that JSON file>
```
