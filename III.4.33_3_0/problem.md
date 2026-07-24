# III.4.33_3_0

## Official Description

> Find the mathematical function skeleton that represents the temperature of the system, given data on the energy of the nth mode of a quantum harmonic oscillator, the Planck constant, the angular frequency of the oscillator, and the Boltzmann constant.

## Data

The training data are stored as a comma-separated file:

| File | Rows |
| --- | ---: |
| `data/train.csv` | 80,000 |

The file contains a header followed by five `float32` columns in this order:

| Column | Role | Official description |
| --- | --- | --- |
| `T` | regression target | the temperature of the system |
| `E_n` | input | the energy of the nth mode of a quantum harmonic oscillator |
| `h` | input | the Planck constant |
| `omega` | input | the angular frequency of the oscillator |
| `kb` | input | the Boltzmann constant |

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
