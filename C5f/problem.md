# C5f: dark matter halo profiles

## Objective

Produce one explicit symbolic expression for $\rho_{\rm NFW/core}$ in terms of $r$, $R_0$, and $x$ that faithfully represents both dark matter halo profiles.

We consider a sixth dataset which is made by combining $C5d$ and $C5e$ to see if the SR algorithms can produce an analytical expression that faithfully represents both profiles. For this dataset, the value of $x$ is crucial for the algorithms to be able to distinguish between the two profiles.

The ground-truth expressions for the two profiles and their combination are intentionally omitted from this problem statement.

## Background

A pressing task in astroparticle physics is determining the distribution of dark matter in large objects such as galaxies. Simulations based on the $\Lambda$CDM model suggest a cuspy matter density profile with an increasing density towards the core of the galaxy. Although galaxies with a cusp profile indeed have been observed, other observations of objects such as dwarf galaxies show a core type density distribution with a constant density near the core.

The density profiles are sensitive to the specific qualities of the dark matter particles such as whether or not they interact through other forces than gravity. Learning more about the dark matter halo profiles of galaxies is one possible step towards a better understanding of dark matter phenomenology. The observational appearance of different dark matter halo density profiles (cusp versus core) for instance prompt the question of whether it is possible to identify another underlying more general density profile that can reconcile the cuspy and core profiles discussed today.

We consider two dark matter halo profiles. One represents a core profile while the other represents the cusp profile. The Navarro-Frenk-White (NFW) density profile represents a cusp profile. $R_0$ is a characteristic radius. We additionally add a classification parameter $x$ as an extra feature which we set to $1$ for the NFW profile and $-1$ for the core profile.

Such an expression extrapolates between two different dark matter density profiles, although using a fabricated classification feature. Since we are here interested in a demonstration benchmark we prefer to consider synthetic datasets with known ground truths and will therefore not consider real dark matter density profile data.

Trend plots: [density against $r$](data/C5de_r.pdf) and [density against $R_0$](data/C5de_R0.pdf).

## Data

Training data: `data/C5f.csv`.

The file contains 20,000 rows and has no added error. $R_0\in[0.5,1.5]$ and $r\in[0.1,2]$ are sampled on uniform grids with $N=100$ in each feature dimension; $x=\pm1$ selects the two profiles.

| Column | Meaning | Observed values or range |
| --- | --- | --- |
| `r` | radial coordinate | 0.1--2.0 |
| `R0` | characteristic radius $R_0$ | 0.5--1.5 |
| `x` | profile classification parameter | $-1$, $1$ |
| `target` | $\rho_{\rm NFW/core}$ | 0.01--13.18359375 |

Use `r`, `R0`, and `x` as features and `target` as the regression target.

## Candidate requirements

The candidate must propose one compact explicit symbolic expression $\widehat{\mathrm{target}}=f(r,R_0,x)$ that represents both $x=1$ and $x=-1$, using optional fitted scalar constants if needed.

Use any analysis you need, but write all generated artifacts only to `<WORKDIR>`. Do not modify `data/C5f.csv`.

The final `ansatz.md` should include the symbolic expression, fitted constants, physical interpretation, full-data MSE, and generated artifacts.

## Scoring rubric

Lower is better.

For $n$ target values $y_i$ and predictions $\hat y_i$, use

$$
\mathrm{MSE}=\frac{1}{n}\sum_{i=1}^{n}(\hat y_i-y_i)^2.
$$

The `<review score="...">` must be the MSE over all 20,000 rows in `data/C5f.csv`; the score direction is **minimize**.

The MSE is simply a measure of the global fit of the symbolic expressions. If an algorithm obtains the correct symbolic equation and the data has no error, the MSE will vanish. A low MSE is not necessarily equal to being close to finding the ground truth since an inherently incorrect expression may be fine-tuned to fit the data well within the training region. Discuss expression simplicity and structural plausibility qualitatively, but do not alter the numeric MSE score.

## Important Notes

- Internet searches are prohibited.
