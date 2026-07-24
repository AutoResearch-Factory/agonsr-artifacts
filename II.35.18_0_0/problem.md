# II.35.18_0_0

## Official Description

> Find the mathematical function skeleton that represents the number of particles at equilibrium, given data on the number of particles in a given state, the Boltzmann constant, the temperature of the system, the magnetic moment of a particle, and the magnetic field strength.

## Data

The training data are stored as a comma-separated file:

| File | Rows |
| --- | ---: |
| `data/train.csv` | 80,000 |

The file contains a header followed by six `float32` columns in this order:

| Column | Role | Official description |
| --- | --- | --- |
| `n_0` | regression target | the number of particles at equilibrium |
| `n` | input | the number of particles in a given state |
| `kb` | input | the Boltzmann constant |
| `T` | input | the temperature of the system |
| `mom` | input | the magnetic moment of a particle |
| `B` | input | the magnetic field strength |

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
