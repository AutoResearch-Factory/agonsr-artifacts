# II.36.38_3_0

## Official Description

> Find the mathematical function skeleton that represents the temperature in Kelvin, given data on the resultant value of the function, the momentum of an object or particle, the magnetic field strength, the Boltzmann constant, the polarizability of a medium or molecule, the electric permittivity of a medium, the speed of light in vacuum, and the magnetization of a material.

## Data

The training data are stored as a comma-separated file:

| File | Rows |
| --- | ---: |
| `data/train.csv` | 80,000 |

The file contains a header followed by nine `float32` columns in this order:

| Column | Role | Official description |
| --- | --- | --- |
| `T` | regression target | the temperature in Kelvin |
| `f` | input | the resultant value of the function |
| `mom` | input | the momentum of an object or particle |
| `H` | input | the magnetic field strength |
| `kb` | input | the Boltzmann constant |
| `alpha` | input | the polarizability of a medium or molecule |
| `epsilon` | input | the electric permittivity of a medium |
| `c` | input | the speed of light in vacuum |
| `M` | input | the magnetization of a material |

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
