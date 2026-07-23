# C3g: cosmic backreaction in a two-region model

## Objective

Recover an explicit symbolic expression for the scaled kinematical backreaction $10^2 Q_D$ in terms of the provided features $H_D$, $v$, and $h$.

Datasets $C3g$ and $C3h$ are included because the targets are here chosen such that we actually know the ground truth expression of the target in terms of the provided features. However, the features are inter-dependent which we suspect may compromise the SR algorithms' ability to identify the ground truth expressions.

The ground-truth expression is intentionally omitted from this problem statement.

## Background

Standard cosmology is based on the assumption that the large-scale dynamics of the Universe can be approximated well by the FLRW models but it has also been discussed whether the structures on smaller scales can affect the large-scale/averaged dynamics. This possibility is known as cosmic backreaction and it has even been suggested that the seemingly accelerated expansion of the Universe is an artifact due to this phenomenon (the co-called backreaction conjecture).

The resulting averaged Hamiltonian constraint and Raychaudhuri equation can be written as (setting $c=1$)

$$
\begin{aligned}
3H_D^2 &= 8\pi G\rho_D - \frac{1}{2}R_D - \frac{1}{2}Q_D\\
3\frac{\ddot a_D}{a_D} &= -4\pi G\rho_D + Q_D.
\end{aligned}
$$

$H_D:=\dot a_D/a_D$ denotes the average Hubble parameter and is related to the local fluid expansion scalar $\theta$ by $H_D=\theta_D/3$ (dots denote derivative with respect to time). $Q_D$ is sometimes referred to as the kinematical backreaction while the deviation of $R_D$ from having FLRW evolution is referred to as intrinsic backreaction.

Two-region models are toy cosmological models consisting of an ensemble of two different FLRW regions. Since the ensemble is disjoint, the model is not an exact solution to Einstein's equation. The model is nonetheless convenient to use for studying backreaction because the model is numerically fast and simple to work with. We will consider a two-region model where one model is the empty (Milne) solution while the other region is an overdense (density larger than the critical density) matter+curvature model.

Here $v$ is the time-dependent volume fraction of the overdense region and $h:=H_o/H_u$.

Trend plot: [C3g](data/C3g.png).

## Data

Training data: `data/C3g.csv`.

The file contains 2,500 rows and has no added error. The data points were generated using equidistant points in the intervals $\langle z\rangle\in[0.1,1]$ and $f_o\in[0.1,0.25]$ with 50 points in both dimensions, giving $50^2$ points in total.

| Column | Meaning | Observed range |
| --- | --- | --- |
| `H` | $H_D$, the average Hubble parameter | 0.0757911208--0.134372246 |
| `h` | $h:=H_o/H_u$ | -2.3186135905--0.2315489836 |
| `v` | time-dependent volume fraction of the overdense region | 0.00884062--0.3981158978 |
| `target` | $10^2 Q_D$ | 0.3720708391--2.6714555562 |

Use `H`, `h`, and `v` as features and `target` as the regression target.

## Candidate requirements

The candidate must propose a compact explicit symbolic expression $\widehat{\mathrm{target}}=f(H,h,v)$ using the available features and optional fitted scalar constants.

Use any analysis you need, but write all generated artifacts only to `<WORKDIR>`. Do not modify `data/C3g.csv`.

The final `ansatz.md` should include the symbolic expression, fitted constants, physical interpretation, full-data MSE, and generated artifacts.

## Scoring rubric

Lower is better.

For $n$ target values $y_i$ and predictions $\hat y_i$, use

$$
\mathrm{MSE}=\frac{1}{n}\sum_{i=1}^{n}(\hat y_i-y_i)^2.
$$

The `<review score="...">` must be the MSE over all 2,500 rows in `data/C3g.csv`; the score direction is **minimize**.

The MSE is simply a measure of the global fit of the symbolic expressions. If an algorithm obtains the correct symbolic equation and the data has no error, the MSE will vanish. A low MSE is not necessarily equal to being close to finding the ground truth since an inherently incorrect expression may be fine-tuned to fit the data well within the training region. Discuss expression simplicity and structural plausibility qualitatively, but do not alter the numeric MSE score.

## Important Notes

- Internet searches are prohibited.
