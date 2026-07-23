# C6c: gravitational-wave-inspired oscillating dataset

## Objective

Recover an explicit symbolic expression for the plus-polarization target $h_+$ in terms of $t$ and $m_1$.

$C6c$ is similar to the dataset $C6a$ except that we now vary an extra model parameter ($m_1$) to see how much the extra feature affects the performance of the SR algorithms.

The ground-truth expression used to generate the mock signal is intentionally omitted from this problem statement.

## Background

Several cosmological datasets represent oscillating behavior, with prime examples being matter power spectra and the power spectrum of the CMB (cosmic microwave background) temperature fluctuations. Another well-known example of oscillating data in astrophysics is that from gravitational waves. We would therefore like our demonstration benchmark to include a dataset exhibiting oscillating behavior.

For this demonstration we prefer datasets with known ground truths since this makes it easier to evaluate the performance of the SR algorithms. We will therefore not consider genuine CMB power spectra, matter power spectrum data or gravitational wave data as these do not represent known analytical expressions we can easily write up. Instead, we will introduce data based on an analytical expression that approximates a (very) simplified gravitational wave signal emitted from the in-spiraling of a two-body system.

We do not claim that the resulting expression for $h_+$ is particularly realistic, but it nonetheless provides us with an oscillating analytical expression inspired by genuine cosmological/astrophysical data. We neglect units since we do not consider this a realistic model and all parameter values are chosen out of convenience rather than physical meaningfulness.

Trend plot: [C6c](data/C6c.pdf).

## Data

Training data: `data/C6c.csv`.

The file contains 10,000 rows and has no added error. For generating this dataset we choose $t\in[0,3]$ and $m_1\in[0.1,1.5]$ and $N=100$ in both dimensions.

| Column | Meaning | Observed range |
| --- | --- | --- |
| `t` | time coordinate; units are neglected | 0.0--3.0 |
| `m1` | model parameter $m_1$ | 0.1--1.5 |
| `target` | plus-polarization signal $h_+$ | -4.1469596514--8.1697104698 |

Use `t` and `m1` as features and `target` as the regression target.

## Candidate requirements

The candidate must propose a compact explicit symbolic expression $\widehat{\mathrm{target}}=f(t,m_1)$ using the available features and optional fitted scalar constants.

Use any analysis you need, but write all generated artifacts only to `<WORKDIR>`. Do not modify `data/C6c.csv`.

The final `ansatz.md` should include the symbolic expression, fitted constants, physical interpretation, full-data MSE, and generated artifacts.

## Scoring rubric

For $n$ target values $y_i$ and predictions $\hat y_i$, use

$$
\mathrm{MSE}=\frac{1}{n}\sum_{i=1}^{n}(\hat y_i-y_i)^2.
$$

Let $N_{free}$ be the number of fitted scalar parameters. The single final score is

$$
\mathrm{Score} = \log_{10}\frac{1}{\mathrm{MSE}} - \max(N_{free}-4,0).
$$

The `<review score="...">` must be this Score over all 10,000 rows in `data/C6c.csv`; the score direction is **maximize**. Every tenfold reduction in MSE adds 1 point, while each fitted parameter beyond 4 subtracts 1 point.

## Important Notes

- Internet searches are prohibited.
- Use at most 4 fitted parameters.
