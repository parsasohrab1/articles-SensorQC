# TRL assessment – SensorQC

**Claimed level: TRL 4** (laboratory validation on public real data with injected faults). Not TRL 5: one station, one year, no real fault labels.

Data: USGS 01579550, 2022, 5-minute values (approved data). Thresholds from the first half-year at a point exceedance rate of 0.001; evaluation on the second half-year.

## False alarms on the unaltered real second half (points per 1000)

| Parameter | Typical 1-day change | rate | residual 2 h | long 1 day | flatline |
|---|---|---|---|---|---|
| Temperature (°C) | 0.74 | 1.08 | 1.61 | 8.95 | 0.34 |
| Specific conductance (µS/cm) | 2.97 | 1.67 | 2.63 | 2.10 | 3.10 |
| Turbidity (FNU) | 0.74 | 0.12 | 0.58 | 0.25 | 35.54 |

## Detection of injected faults (share of 100 injected faults detected per test; 1x / 3x = size in typical one-day changes)

| Parameter | Fault | rate | residual 2 h | long 1 day | flatline |
|---|---|---|---|---|---|
| Temperature (°C) | spike_1x | 1.00 | 0.02 | 0.01 | 0.00 |
| Temperature (°C) | spike_3x | 1.00 | 0.91 | 0.08 | 0.00 |
| Temperature (°C) | step_1x | 1.00 | 0.01 | 0.08 | 0.02 |
| Temperature (°C) | step_3x | 1.00 | 0.92 | 0.31 | 0.00 |
| Temperature (°C) | drift_1x | 0.08 | 0.06 | 0.08 | 0.00 |
| Temperature (°C) | drift_3x | 0.07 | 0.03 | 0.17 | 0.00 |
| Temperature (°C) | flatline | 0.00 | 0.00 | 0.01 | 1.00 |
| Specific conductance (µS/cm) | spike_1x | 0.92 | 0.00 | 0.00 | 0.00 |
| Specific conductance (µS/cm) | spike_3x | 1.00 | 0.03 | 0.00 | 0.00 |
| Specific conductance (µS/cm) | step_1x | 0.97 | 0.00 | 0.00 | 0.00 |
| Specific conductance (µS/cm) | step_3x | 1.00 | 0.07 | 0.01 | 0.00 |
| Specific conductance (µS/cm) | drift_1x | 0.11 | 0.04 | 0.02 | 0.00 |
| Specific conductance (µS/cm) | drift_3x | 0.10 | 0.03 | 0.00 | 0.00 |
| Specific conductance (µS/cm) | flatline | 0.00 | 0.00 | 0.00 | 0.02 |
| Turbidity (FNU) | spike_1x | 0.00 | 0.00 | 0.00 | 0.00 |
| Turbidity (FNU) | spike_3x | 0.00 | 0.00 | 0.00 | 0.00 |
| Turbidity (FNU) | step_1x | 0.00 | 0.01 | 0.00 | 0.41 |
| Turbidity (FNU) | step_3x | 0.00 | 0.00 | 0.00 | 0.44 |
| Turbidity (FNU) | drift_1x | 0.00 | 0.00 | 0.00 | 0.05 |
| Turbidity (FNU) | drift_3x | 0.00 | 0.00 | 0.00 | 0.01 |
| Turbidity (FNU) | flatline | 0.00 | 0.00 | 0.00 | 1.00 |

## Findings and caveats
- Fault sizes here are subtle (1x and 3x the typical daily change). The rate-of-change test catches spikes and steps for temperature and specific conductance (0.92–1.00), but **no test detects drift** at these sizes (at most 0.17), and **none of the tests detects spikes or steps in turbidity** at these sizes: storm events make turbidity so variable that the calibrated thresholds are far above the injected faults.
- The flatline test detects stuck sensors (1.00) for temperature and turbidity but not for specific conductance (0.02: its natural runs of identical values are already long, so the threshold is high), and has a high natural false-alarm rate on turbidity (35 per 1000 points): the sensor often reports identical values in clear water, and run lengths in the second half exceed those of the first half.
- The false-alarm rates on approved data are low (0.1–9 points per 1000) except for the long-window test on temperature (9) and the flatline test on turbidity (35). Approved data were already reviewed by USGS; any point flagged here may simply be a real event.
- Injected faults are an artificial test; real fouling or calibration drift has other shapes. Thresholds from one half-year do not transfer to a different season without care.
- No claim is made that these tests improve on USGS review.
