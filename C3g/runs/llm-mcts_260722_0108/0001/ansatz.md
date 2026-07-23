# One sentence

The proposed no-free-parameter ansatz is

$$
\widehat{\mathrm{target}}=\widehat{10^2Q_D}
=600H_D^2\frac{v(1-v)(1-h)^2}{(1-v+vh)^2}.
$$

# Motivation and explanation

For two disjoint FLRW regions, each region has zero shear and expansion scalar
$\theta_i=3H_i$. The Buchert kinematical backreaction therefore reduces to the
weighted variance of the two regional expansion rates,

$$
Q_D=\frac{2}{3}(\langle\theta^2\rangle_D-\langle\theta\rangle_D^2)
=6v(1-v)(H_o-H_u)^2.
$$

The supplied features eliminate the unobserved regional rates because

$$
H_D=(1-v)H_u+vH_o=H_u(1-v+vh),\qquad h=\frac{H_o}{H_u}.
$$

Hence $H_o-H_u=(h-1)H_D/(1-v+vh)$, and multiplication by the target scaling
$10^2$ gives the stated coefficient $600=10^2\times6$. Thus the final
coefficient and all powers are fixed by the two-region model; there are no
fitted constants in the selected expression.

The expression is dimensionally consistent: $v$, $h$, and $1-v+vh$ are
dimensionless, while $H_D^2$ and $Q_D$ both have dimensions of inverse time
squared. It also enforces $Q_D\geq0$, $Q_D=0$ when either region has zero volume
or when $H_o=H_u$, and quadratic scaling with the expansion-rate contrast. The
denominator is $H_D/H_u$ and ranges from $0.6940674$ to $0.9706614$ in the data,
so no pole is approached on the observed domain.

# Three-step ansatz refinement

All fits used all 2,500 rows and unrounded float64 calculations.

| Iteration | Expression and fitting formulation | Result | Full-data MSE |
| --- | --- | --- | ---: |
| 1 | $AH_D^2v(1-v)(1-h)^2$, raw least squares | $A=891.3535606108$; strong curved residual trend | $4.3902643648\times10^{-2}$ |
| 1 check | Same expression, log least squares | $A=826.4393210491$ | $5.452482\times10^{-2}$ |
| 2 | $AH_D^2v(1-v)(1-h)^2/(1-v+vh)^p$, raw least squares | $A=600.0000000134$, $p=1.99999999997$ | $8.9455533848\times10^{-19}$ |
| 2 check | Same expression, log/relative least squares | $A=600.0000000290$, $p=1.99999999984$ | $8.9477361466\times10^{-19}$ |
| 2 check | Same expression, relative soft-$L_1$ loss | $A=600.0000000282$, $p=1.99999999984$ | $8.9475314153\times10^{-19}$ |
| 3 diagnostic | Free powers $AH_D^\alpha v^\beta(1-v)^\gamma\lvert1-h\rvert^\delta/(1-v+vh)^\epsilon$, log-linear fit | $(\alpha,\beta,\gamma,\delta,\epsilon)=(2.0000000011,0.9999999996,1.0000000024,1.9999999999,2.0000000054)$ | $8.9309273290\times10^{-19}$ |
| 3 selected | Theory-constrained powers and fixed $A=600$ | No fitted constants | $8.9509122221\times10^{-19}$ |

Iteration 1 captures the variance prefactor but incorrectly treats the supplied
$H_D$ as a regional rate. Iteration 2 supplies the necessary conversion from
$H_D$ to $H_u$; all four objectives independently recover $p=2$ and $A=600$.
Iteration 3 allows every power to vary as a diagnostic and recovers the integer
powers to about $10^{-8}$ or better. Its tiny MSE advantage over the fixed form
is only a fit to decimal rounding and does not justify six parameters.

# Performance and robustness

For the selected fixed expression on all 2,500 rows:

| Metric | Value |
| --- | ---: |
| MSE | $8.950912222145613\times10^{-19}$ |
| RMSE | $9.4609260763\times10^{-10}$ |
| MAE | $7.7632805111\times10^{-10}$ |
| Maximum absolute error | $3.0901342596\times10^{-9}$ |
| Maximum relative error | $5.3480182492\times10^{-9}$ |
| Mean signed error | $-2.3320334219\times10^{-11}$ |

As a coefficient-sensitivity check, retaining the theory-constrained structure
but fitting only $A$ gives $A=600.0000000096221$ under raw least squares and MSE
$8.9456471666\times10^{-19}$. Log, relative, and robust-relative fits give
$A=600.0000000130$--$600.0000000132$. These changes are negligible and are
consistent with the finite decimal precision of the CSV, so $A=600$ is the
better-supported value.

The standardized design matrix for the five-power diagnostic has condition
number $55.26$, reflecting the stated feature dependence. In 400 deterministic
tests with multiplicative target perturbations of log-standard-deviation
$10^{-6}$, the widest 95% power interval was for the denominator exponent,
$\epsilon\in[1.99999098,2.00000992]$; the constrained amplitude had standard
deviation $1.22\times10^{-5}$. The physical derivation avoids this unnecessary
conditioning. The worst-case table and residual plot show no residual structure
beyond the approximately $10^{-9}$ rounding floor.

# Reproduction and artifacts

Run the analysis from this directory with

```bash
timeout 600 python3 fit_ansatz.py
timeout 600 pytest -q test_fit_ansatz.py
```

Ruff 0.15.22 was used for linting; the numerical environment and exact package
versions are recorded in `fit_results.json`. No problem-local `.venv` was
present, so the available system Python 3.12.3 environment was used.

- `fit_ansatz.py`: deterministic three-iteration fitting, sensitivity analysis,
  metrics, and plotting.
- `test_fit_ansatz.py`: tests the two-region algebraic identity, scalar fitting
  objectives, and metric calculation.
- `candidate_metrics.csv`: metrics and parameters for every candidate and
  objective.
- `fit_results.json`: complete machine-readable fit results, data ranges,
  conditioning, perturbation settings, seed, and environment versions.
- `final_parity_residuals.png`: annotated final parity and residual plot.
- `iteration_residuals.png`: residual comparison across the three refinements.
- `exponent_sensitivity.csv` and `exponent_sensitivity.png`: generalized-power
  recovery and perturbation sensitivity.
- `worst_cases.csv`: the 20 largest absolute residuals for the selected fixed
  expression.

# Difficulties and open questions

The main difficulty was that $H_D$, $h$, and $v$ are interdependent, so an
empirical power fit could imitate the data without identifying why the
denominator is present. Rewriting the regional variance in terms of $H_D$
resolved this and fixed every coefficient and exponent. There is no unresolved
question about the expression on the stated two-region assumptions; outside
that setting, regional shear or more than two regional expansion rates would
require additional terms and are not identifiable from this dataset alone.

<review score="8.950912222145613e-19">
**Verdict.** The candidate is valid, dimensionally consistent, structurally
well justified, and essentially exact to the precision of the supplied CSV. I
found no critical issue, constraint violation, leakage relevant to the stated
rubric, or unsupported scoring claim.

**Independent score check.** I loaded all 2,500 rows of `data/C3g.csv` and
evaluated the selected expression directly in float64, independently of the
candidate's metric helper. This reproduced

\[
\operatorname{MSE}=\frac{1}{2500}\sum_i(\hat y_i-y_i)^2
=8.950912222145613\times10^{-19}.
\]

The accompanying diagnostics also reproduce: RMSE
\(9.4609260763\times10^{-10}\), MAE \(7.7632805111\times10^{-10}\), maximum
absolute error \(3.0901342596\times10^{-9}\), and mean signed error
\(-2.3320334219\times10^{-11}\). Thus the candidate has reported MSE, not
RMSE, squared norm, or an MSE subtotal. The residual plots are consistent with
a rounding-scale cloud; as a limited numerical check, the largest absolute
Pearson correlation of the residual with any of \(H,h,v,\mathrm{target}\) is
only 0.0119. The three supplied tests pass.

At this extremely small residual scale, reassociating algebraically equivalent
float64 operations changes the MSE by about \(1.6\times10^{-26}\); exact-decimal
evaluation lies between those float64 results. This is ordinary roundoff after
near-cancellation, not a substantive metric discrepancy. The score above uses
the candidate's explicit recorded evaluation order and is exactly
reproducible from its artifacts.

**Physics, dimensions, and domain.** The standard Buchert definition gives
\(Q_D=\frac23(\langle\theta^2\rangle_D-\langle\theta\rangle_D^2)
-2\langle\sigma^2\rangle_D\) (see
[Buchert 2001, Eq. 13c](https://arxiv.org/pdf/gr-qc/0102049)). Each constituent
FLRW region is shear-free and has \(\theta_i=3H_i\), so the two-component
weighted-variance identity indeed yields
\(Q_D=6v(1-v)(H_o-H_u)^2\). Substitution of
\(H_D=H_u(1-v+vh)\) and \(h=H_o/H_u\) gives exactly the proposed formula,
including the coefficient \(600=100\times6\) and denominator power two.

The factors \(v\), \(h\), and \(1-v+vh\) are dimensionless, while \(H_D^2\)
has the same inverse-time-squared dimension as \(Q_D\). Hence there is no
dimensional-consistency penalty. The denominator is positive on every row and
has independently verified range \([0.6940674337,0.9706613983]\), so the
formula has no sampled pole or undefined prediction.

**Simplicity and parameter accounting.** The selected expression has no fitted
scalar parameter. Although the candidate explored fitted amplitudes and powers
as diagnostics, the final coefficient and powers are independently fixed by
the physical derivation above, so those diagnostics do not turn them into
hidden fitted parameters. The run lineage contains only the root and this
candidate, with no ancestor or sibling search from which additional hard-coded
choices could have been imported. The use of the complete dataset is also what
the rubric explicitly requires for the score; the generalized fitted forms are
not the selected ansatz.

**Score accounting.** The rubric has one numeric component: full-data MSE
\(=8.950912222145613\times10^{-19}\). Therefore the component sum and final
total score are both **\(8.950912222145613\times10^{-19}\)** (lower is better).
</review>
