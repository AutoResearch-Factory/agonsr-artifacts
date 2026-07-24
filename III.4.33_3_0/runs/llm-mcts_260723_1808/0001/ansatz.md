## One sentence

The proposed zero-fit-parameter ansatz is
\[
T(E_n,h,\omega,k_b)=\frac{h\omega}{2\pi k_b\log(1+\frac{h\omega}{2\pi E_n})},
\]
implemented as `q = h*omega/(2*pi)` and `T = q/(kb*log1p(q/E_n))`.

## Motivation and explanation

Let
\[
q=\hbar\omega=\frac{h\omega}{2\pi}.
\]
For a thermally populated quantum harmonic-oscillator mode, with the
zero-point contribution excluded from the reported excitation energy,
\[
E_n=\frac{q}{\exp(q/(k_bT))-1}.
\]
Solving this relation for \(T\) gives the proposed expression exactly:
\[
\exp(q/(k_bT))=1+\frac{q}{E_n},
\qquad
T=\frac{q}{k_b\log(1+q/E_n)}.
\]
The factor \(2\pi\) is required because the input is the Planck constant
\(h\), while an angular frequency couples to the reduced Planck constant
\(\hbar=h/(2\pi)\). Treating \(h\) as though it were \(\hbar\) gives NRMSE
\(0.4095\), compared with \(7.42\times10^{-8}\) for the proposed form.

This expression is dimensionally consistent: \(q\) and \(E_n\) are energies,
so \(q/E_n\) and the logarithm argument are dimensionless; \(q/k_b\) has
units of temperature. The known constant \(2\pi\) is not a fitted parameter,
so the ansatz uses zero of the four allowed parameters.

For \(E_n,h,\omega,k_b>0\), write \(L=\log(1+q/E_n)>0\). The expression
satisfies the physically useful constraints
\[
\frac{\partial T}{\partial E_n}
=\frac{q^2}{k_bE_n(E_n+q)L^2}>0,
\qquad
\frac{\partial T}{\partial q}
=\frac{L-q/(E_n+q)}{k_bL^2}>0,
\qquad
\frac{\partial T}{\partial k_b}=-\frac{T}{k_b}<0.
\]
The second inequality follows from
\(\log(1+z)>z/(1+z)\) for \(z>0\). In the classical limit,
\[
\lim_{q/E_n\to0}T=\frac{E_n}{k_b}.
\]
The saved grid checks cover 12 orders of magnitude in each positive
quantity and confirm positivity, these monotonicities, energy-unit
invariance, and the classical limit. Numerically, `log1p` should be used to
preserve the small-\(q/E_n\) limit.

## Performance

On all 80,000 training rows, evaluated in float64 with `log1p`:

| Metric | Result |
| --- | ---: |
| RMSE | \(2.91038\times10^{-7}\) |
| NRMSE | \(7.41978\times10^{-8}\) |
| Score | \(7.129609\) |
| MAE | \(1.83949\times10^{-7}\) |
| Mean residual | \(1.48661\times10^{-9}\) |
| Maximum absolute error | \(2.97191\times10^{-6}\) |
| Maximum relative error | \(1.54908\times10^{-7}\) |

The dimensionless ratio \(q/E_n\) ranges from \(0.007173\) to \(11.6822\),
so the data test both near-classical and strongly quantum regimes. The
residual bias is negligible in every ratio decile. Decile RMSE decreases
from \(3.91\times10^{-7}\) to \(6.18\times10^{-8}\); the corresponding
within-decile scores range from 7.017 to 7.168. The absolute-error trend is
consistent with float32 decimal quantization because the largest
temperatures occur mostly in the small-\(q/E_n\) regime.

### Iteration 1: theory screen

| Candidate | NRMSE | Score |
| --- | ---: | ---: |
| Proposed inverse Planck law using \(\hbar=h/(2\pi)\) | \(7.41978\times10^{-8}\) | 7.129609 |
| Classical limit \(E_n/k_b\) | \(8.93705\times10^{-2}\) | 1.048806 |
| Inverse Planck law incorrectly using \(h\omega\) | \(4.09501\times10^{-1}\) | 0.387745 |

This iteration isolated the \(2\pi\) conversion and showed that the result
is not merely an equipartition approximation.

### Iteration 2: calibrated variants and fitting objectives

I fitted
\[
T=\frac{A h\omega}{k_b\log(1+B h\omega/E_n)}
\]
with positive \(A,B\), using a fixed interleaved 80/20 train/validation
split. Direct-\(T\), relative-error, log-\(T\), and robust direct objectives
were tested, along with the constrained one-parameter case \(A=B=c\).

| Validation formulation | Parameters | \(A\) | \(B\) | NRMSE | Score | Jacobian condition |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| One-parameter direct | 1 | 0.1591549420 | 0.1591549420 | \(7.29985\times10^{-8}\) | 7.136686 | 1.0 |
| Two-parameter direct | 2 | 0.1591549418 | 0.1591549418 | \(7.30008\times10^{-8}\) | 7.136673 | 62.1 |
| Two-parameter log/relative | 2 | 0.1591549431 | 0.1591549431 | \(7.30107\times10^{-8}\) | 7.136613 | 21.3 |
| Fixed \(A=B=1/(2\pi)\) | 0 | 0.1591549431 | 0.1591549431 | \(7.30120\times10^{-8}\) | 7.136606 | not applicable |

The best fitted validation NRMSE improves on the fixed theory by only
0.0185%, or \(0.000080\) score units. The fitted direct constant differs
from \(1/(2\pi)\) by \(1.07\times10^{-9}\); relative and log objectives
recover the theoretical value within \(1.3\times10^{-11}\). Separating
\(A\) and \(B\) adds no meaningful accuracy and worsens conditioning.
Robust direct fitting reaches the same conclusion, with condition number
53.9. These objective-dependent shifts are far below the input precision
and are not defensible new physical parameters.

### Iteration 3: stability, numerical precision, and failure modes

Ten deterministic held-out folds were used to refit the constrained direct
constant. Its relative deviation from \(1/(2\pi)\) ranged from \(-13.48\)
to \(-7.14\) parts per billion, with mean \(-9.99\) and standard deviation
2.30 parts per billion. This is an empirical stability envelope rather than
a formal confidence interval: the folds overlap and the remaining error is
deterministic float32 quantization, not independent measurement noise.

Float64 `log1p`, plain-log, and algebraically rearranged evaluations all
give score 7.129609 over the observed ratio range. Native float32
evaluation lowers the score to 6.937771 and increases maximum absolute
error to about \(4\times10^{-6}\). Thus float64 `log1p` is the preferred
implementation. Plain `log(1+z)` is a failure mode under extrapolation to
much smaller \(z=q/E_n\), even though the current minimum \(z\) is large
enough that its observed score is unchanged. Nonpositive physical inputs
are outside the ansatz domain.

The exact-theory form is therefore preferred over fitted alternatives:
it has fewer parameters, the correct dimensions and limits, superior
conditioning, and performance already at the precision floor of the data.

## Artifacts

- `iteration1_theory.py`: reproducible theory-candidate evaluation.
- `iteration1_candidate_metrics.csv`: candidate comparison table.
- `iteration1_data_summary.csv`: input ranges and dimensionless-regime range.
- `iteration1_parity_residuals.png`: parity and residual-regime diagnostic;
  the displayed formula states that there are no fitted parameters.
- `iteration2_calibration.py`: constrained and unconstrained fits under
  direct, relative, log, and robust losses.
- `iteration2_fit_metrics.csv`: train, validation, and all-data fit metrics,
  coefficients, deviations from theory, and Jacobian condition numbers.
- `iteration2_calibrated_parity.png`: validation-selected calibration parity
  plot with its ansatz and parameter values shown.
- `iteration3_robustness.py`: cross-fold, numerical-precision, regime,
  worst-case, and analytic-constraint checks.
- `iteration3_numerical_formulations.csv`: implementation sensitivity.
- `iteration3_crossfold_stability.csv`: ten-fold coefficient stability and
  held-out errors.
- `iteration3_regime_metrics.csv`: residual metrics by \(q/E_n\) decile.
- `iteration3_worst_cases.csv`: the 25 largest absolute residuals.
- `iteration3_constraint_checks.csv`: positivity, monotonicity, dimensional
  scale-invariance, and limiting-behavior results.
- `iteration3_robustness.png`: consolidated robustness diagnostics with the
  final formula and zero fitted parameters shown.

The scripts ran with Python 3.12.3, NumPy 1.26.4, pandas 2.1.4, SciPy
1.11.4, and Matplotlib 3.6.3. No problem-local `.venv` executable was
present, so the available system environment was used. Each script was run
with a 600-second timeout and completed in under one second. `ruff` was not
installed; all scripts were syntax-checked with `py_compile` and executed
end to end.

The main difficulty was distinguishing \(h\) from \(\hbar\) and deciding
whether part-per-billion fitted shifts represented real calibration.
Angular-frequency dimensional reasoning resolved the former; multi-loss
fits, conditioning checks, cross-fold stability, and float32 diagnostics
showed that the latter are numerical artifacts. The only interpretive open
question is terminology: the data behave as though \(E_n\) is the thermal
mode energy with the zero-point contribution excluded. If a future dataset
defines \(E_n\) as total oscillator energy including
\(\hbar\omega/2\), the inversion would need to be revised.

<review score="7.140062">
**Final score: 7.140062.**

**Independent held-out evaluation.** I evaluated the displayed
zero-parameter expression directly in float64 using `log1p`, without any
held-out calibration. The diagnostic NRMSE is
\(7.243320635039751\times10^{-8}\), so the problem's sole score is
\[
\log_{10}(1/\mathrm{NRMSE})
=7.140062289761816,
\]
which rounds to the score in the review attribute. The corresponding
diagnostic RMSE is \(2.835823369555691\times10^{-7}\). Vectorized summation
and an independent scalar `fsum` calculation agreed at the shown precision.

**Correctness and constraints.** The expression is dimensionally
consistent: \(h\omega/(2\pi)\) and \(E_n\) are energies, the logarithm has a
dimensionless argument, and division by \(k_b\) leaves temperature. The
algebraic inversion, stated derivatives, positivity, monotonicities, and
classical limit are correct for positive inputs. The factor \(1/(2\pi)\) is
the exact conversion from the supplied Planck constant \(h\) to \(\hbar\)
when paired with angular frequency, so it is theoretically fixed rather
than a fitted parameter. The final ansatz therefore has zero fitted
parameters and satisfies the four-parameter limit.

**Evidence audit.** Independent recomputation reproduces the reported
training metrics, and the scripts use the NRMSE and logarithmic score
definitions from the problem rather than an MSE or mislabeled \(L_2\)
quantity. The saved fit, regime, precision, and constraint tables are
consistent with the claims made from them. The run tree contains no
ancestor or sibling candidates indicating cross-node tuning; calibrated
constants appear only in diagnostics and are not used in the scored
formula. The attribution of the remaining error specifically to float32
quantization is plausible but not established causally by the supplied
checks, and the zero-point interpretation of \(E_n\) remains terminological;
neither caveat changes the evaluated formula or score.
</review>
