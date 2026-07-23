# PO39

## Official Description

> Find the mathematical function skeleton that represents Acceleration in Nonl-linear Harmonic Oscillator, given data on Position at time t, Time, and Velocity at time t.

## Data

The training data are stored as a comma-separated file:

| File | Rows |
| --- | ---: |
| `data/train.csv` | 4,000 |

The file contains a header followed by four `float32` columns in this order:

| Column | Role | Official description |
| --- | --- | --- |
| `dv_dt` | regression target | Acceleration in Nonl-linear Harmonic Oscillator |
| `x` | input | Position at time t |
| `t` | input | Time |
| `v` | input | Velocity at time t |

## Metric

For targets $y_i$ and predictions $\hat y_i$, define

$$
\mathrm{NRMSE} = \sqrt{\frac{\sum_i (\hat y_i-y_i)^2}{\sum_i (y_i-\bar y)^2}}.
$$

The single final score is

$$
\mathrm{Score} = \log_{10} \frac{1}{\mathrm{NRMSE}}.
$$

Higher is better. Every tenfold reduction in NRMSE adds 1 point.

## Important Notes

- Internet searches are prohibited.
- Use at most 4 fitted parameters.
