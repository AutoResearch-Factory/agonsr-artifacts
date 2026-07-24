# II.6.15a_2_0

## Official Description

> Find the mathematical function skeleton that represents the distance from the dipole to the point where the field is being measured, given data on the electric field strength at a point, the electric constant (permittivity of free space), the electric dipole moment, the x-coordinate of the point where the field is being measured, the y-coordinate of the point where the field is being measured, and the z-coordinate of the point where the field is being measured.

## Data

The training data are stored as a comma-separated file:

| File | Rows |
| --- | ---: |
| `data/train.csv` | 80,000 |

The file contains a header followed by seven `float32` columns in this order:

| Column | Role | Official description |
| --- | --- | --- |
| `r` | regression target | the distance from the dipole to the point where the field is being measured |
| `Ef` | input | the electric field strength at a point |
| `epsilon` | input | the electric constant (permittivity of free space) |
| `p_d` | input | the electric dipole moment |
| `x` | input | the x-coordinate of the point where the field is being measured |
| `y` | input | the y-coordinate of the point where the field is being measured |
| `z` | input | the z-coordinate of the point where the field is being measured |

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
