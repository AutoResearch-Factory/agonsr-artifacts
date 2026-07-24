## One sentence

The proposed parameter-free ansatz is

$$
x=\frac{\mathrm{mom}B}{k_bT}, \qquad
n_0=n[\exp(x)+\exp(-x)]=2n\cosh(x).
$$

## Motivation and explanation

The magnetic energy scale is $\mathrm{mom}B$, while the thermal energy
scale is $k_bT$, so their ratio $x$ is the dimensionless variable that may
appear in a Boltzmann factor. The two magnetic orientations contribute
$n\exp(x)$ and $n\exp(-x)$; summing their populations gives the proposed
expression. No fitted parameters are needed.

The expression satisfies the relevant physical constraints by
construction:

- Dimensional consistency: $[\mathrm{mom}B]=[k_bT]$ (energy), so $x$ is
  dimensionless and $n_0$ has the same units as $n$.
- Positivity and extensivity: $n_0>0$ for $n>0$, and $n_0$ is linear in
  $n$.
- Zero-field limit: $n_0(B=0)=2n$.
- State-exchange symmetry: reversing the sign of $B$ or of the magnetic
  moment leaves $n_0$ unchanged.
- Field dependence: $n_0$ increases monotonically with $|x|$ and has the
  large-field limit $n_0\sim n\exp(|x|)$.

### Three ansatz revisions

All fits used a fixed seed of 3518 and an 80/20 train/validation split.
Each revision was fitted with direct target residuals, log-target
residuals, and soft-$L_1$ relative residuals.

| Revision | Expression | Best validation NRMSE | Best validation score |
| --- | --- | ---: | ---: |
| 1: one branch | $a n\exp(bx)$ | $1.4016\times10^{-2}$ | 1.853384 |
| 2: asymmetric branches | $n[a_+\exp(bx)+a_-\exp(-bx)]$ | $3.3201\times10^{-7}$ | 6.478853 |
| 3: symmetric branches | $a n[\exp(bx)+\exp(-bx)]$ | $3.3302\times10^{-7}$ | 6.477528 |
| Final theory | $n[\exp(x)+\exp(-x)]$ | $3.3312\times10^{-7}$ | 6.477401 |

The one-branch model misses the second state and fails especially near
small $x$. Adding the second branch removes the structural residual.
Under the robust-relative objective, its fitted coefficients are

$$
a_+=1.0000000006,\qquad b=0.999999999714,\qquad
a_-=0.999999997782.
$$

State-exchange symmetry then reduces the model to two fitted
coefficients. The log-objective fit gives

$$
a=0.999999999940,\qquad b=0.999999999990.
$$

These results support fixing every coefficient to its theoretical value
of one. The asymmetric fit's score advantage over the parameter-free
law is only 0.00145, corresponding to a roughly 0.33% NRMSE change at
the float32 rounding floor, and does not justify three free parameters.

## Performance

For the final parameter-free expression:

| Split | Rows | NRMSE | Score | Median absolute relative error | 99th percentile | Maximum |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fit/train | 64,000 | $3.0745\times10^{-7}$ | 6.512221 | $3.9670\times10^{-8}$ | $2.8298\times10^{-7}$ | $8.1922\times10^{-7}$ |
| Validation | 16,000 | $3.3312\times10^{-7}$ | 6.477401 | $3.9683\times10^{-8}$ | $2.7441\times10^{-7}$ | $8.3279\times10^{-7}$ |
| All data | 80,000 | $3.1970\times10^{-7}$ | 6.495255 | $3.9670\times10^{-8}$ | $2.8135\times10^{-7}$ | $8.3279\times10^{-7}$ |

The data cover $0.13635\le x\le7.8270$ and
$0.013756\le n_0\le3213.8291$. Direct least squares is poorly balanced
over this range: its final-model Jacobian condition number is 25.04,
versus 2.85 for the log fit, and its fitted coefficients vary by about
$2\times10^{-7}$ across half-samples. Log and robust-relative fits vary
only at roughly the $10^{-9}$ level. The log formulation is therefore
the better coefficient-identification check, even though the official
metric itself is evaluated in the original target space.

The local log-fit standard errors are $4.84\times10^{-10}$ for $a$ and
$3.63\times10^{-10}$ for $b$. These quantify numerical consistency, not
independent physical measurement uncertainty. The float64 forms
$\exp(x)+\exp(-x)$, $2\cosh(x)$, and the factored positive-$|x|$ form
give identical scores and differ in prediction by at most
$9.1\times10^{-13}$. Float32 evaluation is less accurate
(all-data score 6.3776), so float64 evaluation is recommended.

Residuals grow mildly with $x$ but remain at the expected float32 input
and target quantization scale, without evidence for a missing term.
Behavior outside the sampled positive-input range is theory-guided
rather than empirically tested; the even dependence on $x$ supplies the
physically required negative-field continuation.

## Artifacts

- `analyze_ansatz.py`: reproducible loading, three-iteration fitting,
  objective comparison, stability refits, metrics, and plotting.
- `test_analyze_ansatz.py`: focused formula and metric unit tests.
- `diagnostics.png`: annotated final parity plot, residuals versus $x$,
  binned residual tails, and revision scores.
- `metrics.csv`: train, validation, and all-data metrics for every
  candidate and objective.
- `data_summary.csv`: variable ranges and quantiles.
- `parameter_stability.csv`: full-fit conditioning, local standard
  errors, and five fixed-seed half-sample refits per objective.
- `numerical_forms.csv`: comparison of algebraically equivalent float64
  forms and float32 evaluation.
- `worst_residuals.csv`: the 25 largest final relative residuals with
  their inputs.

Reproduction commands:

```bash
timeout 600 python3 analyze_ansatz.py
timeout 600 python3 -m unittest -v test_analyze_ansatz.py
python3 -m py_compile analyze_ansatz.py test_analyze_ansatz.py
```

The problem workspace has no executable `.venv`, so the available
system Python 3.12.3 was used with NumPy 1.26.4, SciPy 1.11.4, and
Matplotlib 3.6.3. All three tests pass. `ruff` was not installed, so
linting could not be run; compilation and unit tests found no errors.
The main modeling difficulty was the target's large dynamic range,
which made direct fitting sensitive to a few extreme rows. Log and
robust-relative fits resolved the conditioning issue and showed that
the remaining discrepancies are rounding-scale noise. There are no
material open questions for the symbolic skeleton.

<review score="6.441936561481">
**Final score: 6.441936561481.**

**Independent held-out evaluation.** I evaluated the stated final law
$n_0=n[\exp(x)+\exp(-x)]$, with
$x=\mathrm{mom}B/(k_bT)$, in float64 and applied the problem's exact
metric. The held-out NRMSE is $3.614626585699\times10^{-7}$, hence
$\log_{10}(1/\mathrm{NRMSE})=6.441936561481$. The problem defines only
this single score: NRMSE is a diagnostic, and 6.441936561481 is both the
metric result and the final total, with no separate component score to
add.

**Scientific and constraint audit.** The expression is dimensionally
consistent: $\mathrm{mom}B$ and $k_bT$ are energies, so the exponential
arguments are dimensionless, and multiplying by $n$ gives $n_0$ the
units of a particle count. The final expression has zero fitted
parameters and therefore satisfies the four-parameter limit. The unit
Boltzmann slope, opposite signs, and equal branch weights are fixed by
the stated two-state physical argument rather than retained fitted
constants. The run contains no ancestor or sibling candidate carrying
alternative tuned constants, and I found no hidden numerical
model-selection parameter.

**Evidence and claim checks.** The candidate analysis references the
training set only; I found no held-out access or leakage in its code.
An independent calculation using the algebraically equivalent
$2n\cosh(x)$ form gives the same held-out score to numerical summation
precision. I also reproduced the reported all-training score
(6.495255227904 independently versus 6.495255227905 reported), and all
three supplied unit tests pass. The fitted coefficients' convergence
to unity supports, but is not needed to define, the final
parameter-free law. Claims about negative fields and behavior beyond
the sampled regime remain theory-based extrapolations, as the candidate
already acknowledges; this is not a dimensional or scoring failure.
No critical issue was found.
</review>
