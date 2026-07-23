# I.32.17_4_3

## Official Description

> Find the mathematical function skeleton that represents the frequency of the external electric field, given data on the power of the scattered radiation, the electric constant (permittivity of free space), the speed of light, the strength of the external electric field, the radius of the scattering object or atom, and the natural frequency of the oscillator or resonant frequency.

## Data

The training data are stored as a comma-separated file:

| File | Rows |
| --- | ---: |
| `data/train.csv` | 80,000 |

The file contains a header followed by seven `float32` columns in this order:

| Column | Role | Official description |
| --- | --- | --- |
| `omega` | regression target | the frequency of the external electric field |
| `Pwr` | input | the power of the scattered radiation |
| `epsilon` | input | the electric constant (permittivity of free space) |
| `c` | input | the speed of light |
| `Ef` | input | the strength of the external electric field |
| `r` | input | the radius of the scattering object or atom |
| `omega_0` | input | the natural frequency of the oscillator or resonant frequency |

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
