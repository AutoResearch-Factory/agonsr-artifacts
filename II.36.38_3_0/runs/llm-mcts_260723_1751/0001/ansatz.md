## One sentence

The proposed zero-parameter ansatz is
$$
T=\frac{\mathrm{mom}}{k_b f}(H-\frac{\alpha M}{\epsilon c^2}).
$$

## Motivation and explanation

Define the effective magnetic field
$$
H_{\mathrm{eff}}=H-\frac{\alpha M}{\epsilon c^2}.
$$
The data support the dimensionless forward relation
$$
f=\frac{\mathrm{mom}H_{\mathrm{eff}}}{k_bT},
$$
whose explicit inversion gives the proposed ansatz. The subtraction is
essential: it explains both signs of \(T\) and the observed zero crossing at
\(H=\alpha M/(\epsilon c^2)\).

The discovery was checked in three iterations:

1. An additive effective-field screen failed; even after an affine diagnostic
   calibration its best NRMSE was about \(0.68\). Inspecting the signed
   cancellation exposed the subtractive form.
2. The three-parameter discovery family
   $$
   T=\frac{\mathrm{mom}}{k_bf}(a_HH+
   a_M\frac{\alpha M}{\epsilon c^{p_c}})
   $$
   was fitted using direct \(T\)-residuals, field-scaled residuals, and robust
   soft-L1 residuals. All three gave \(a_H=1\), \(a_M=-1\), and \(p_c=2\) to
   approximately eight decimal places. An independent exponent profile has a
   sharp minimum at \(p_c=2\).
3. Fixing the exact coefficients removed all fitted parameters. Residual,
   worst-case, cancellation, implementation-order, subsampling, and synthetic
   noise checks found no missing structure.

The formula is dimensionally consistent under the physical interpretation
implied by the variables. Since \(1/(\epsilon c^2)\) has permeability units,
\(\alpha M/(\epsilon c^2)\) has the same field units as \(H\) when \(\alpha\)
is dimensionless. Interpreting `mom` as a magnetic moment makes
\(\mathrm{mom}H_{\mathrm{eff}}\) an energy; division by \(k_b\) gives kelvin,
and \(f\) is dimensionless. The official phrase “momentum” for `mom` is
therefore likely generic or imprecise; literal mechanical momentum would not
give a dimensionally consistent relation with the supplied variables.

For positive inputs, the construction also gives useful behavior directly:

- \(T=0\) at magnetic compensation,
  \(H=\alpha M/(\epsilon c^2)\).
- \(T\) increases with \(H\), decreases with \(\alpha\) and \(M\), and
  increases with \(\epsilon\) and \(c\).
- As \(\alpha\to0\), \(M\to0\), \(\epsilon\to\infty\), or \(c\to\infty\),
  the expression reduces to \(T=\mathrm{mom}H/(k_bf)\).
- The derivatives with respect to \(f\) and \(k_b\) are \(-T/f\) and
  \(-T/k_b\), so their monotonic direction changes consistently with the sign
  of the effective field.
- The expression is defined whenever \(k_bf\epsilon c^2\ne0\); all training
  rows are safely inside this domain.

## Performance

The selected ansatz has **zero fitted parameters**, below the four-parameter
limit.

| Evaluation | NRMSE | Score | RMSE | MAE | Maximum absolute error |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fixed formula, all 80,000 rows | \(8.4943\times10^{-8}\) | 7.07087 | \(9.9353\times10^{-8}\) | \(3.6836\times10^{-8}\) | \(4.9409\times10^{-6}\) |
| Fixed formula, 20,000-row holdout | \(8.5952\times10^{-8}\) | 7.06574 | — | — | \(4.9409\times10^{-6}\) |
| Three-parameter direct fit, holdout | \(8.5689\times10^{-8}\) | 7.06708 | — | — | — |

The fitted form improves the holdout score by only \(0.0013\), an amount
consistent with float32 CSV rounding, so its three near-integer parameters are
not justified. For comparison, replacing \(c^2\) by \(c\) gives NRMSE
\(0.3788\), omitting the magnetization correction gives \(0.6739\), and using
the wrong plus sign gives \(1.3477\).

For the fixed formula on all rows, the residual bias is
\(-1.67\times10^{-10}\). The median, 99th-percentile, and maximum absolute
residuals are \(1.36\times10^{-8}\), \(4.07\times10^{-7}\), and
\(4.94\times10^{-6}\). Float64 algebraic evaluation orders agree to negligible
precision; explicit float32 evaluation is slightly worse, confirming that the
remaining error is numerical rather than structural.

The discovery coefficients are stable. Across twelve independent 1,000-row
subsamples with no added noise, their mean and standard deviation were
\(a_H=0.999999995\pm2.4\times10^{-8}\),
\(a_M=-1.000000003\pm5.2\times10^{-8}\), and
\(p_c=2.000000061\pm4.1\times10^{-8}\). With Gaussian target noise at 1% of
the global \(T\) standard deviation and 20,000-row subsamples, the corresponding
estimates remained
\(0.999968\pm5.8\times10^{-5}\),
\(-1.000012\pm1.5\times10^{-4}\), and
\(2.000127\pm2.6\times10^{-4}\).

## Artifacts

- `iteration1_screen.py`, `iteration1_report.txt`,
  `iteration1_summary.csv`, `iteration1_dependence.csv`,
  `iteration1_candidate_screen.csv`, and `iteration1_univariate.png`:
  numerical characterization and initial candidate screen.
- `iteration2_fit.py`, `iteration2_report.txt`,
  `iteration2_formulations.csv`, `iteration2_candidate_comparison.csv`,
  `iteration2_exponent_profile.csv`, and
  `iteration2_exponent_profile.png`: multi-objective coefficient fitting,
  ablations, and exponent identification.
- `iteration3_diagnostics.py`, `iteration3_report.txt`,
  `iteration3_implementation_comparison.csv`,
  `iteration3_residual_quantiles.csv`,
  `iteration3_cancellation_bins.csv`, `iteration3_worst_cases.csv`,
  `iteration3_stability_trials.csv`, `iteration3_stability_summary.csv`,
  `iteration3_parity_residuals.png`, and `iteration3_stability.png`: final
  residual, numerical, constraint-regime, and robustness diagnostics.

All scripts use the fixed seed 20260723 and read only the problem's
`data/train.csv`. No external dependencies were introduced. The only open
physical question is whether the official label “momentum” should instead read
“magnetic moment”; it does not affect the numerically identified skeleton.

<review score="7.096406336739107">
Independent evaluation of the formula exactly as written, using float64
arithmetic on all 20,000 designated held-out rows, gives
\(\mathrm{NRMSE}=8.009283441978657\times10^{-8}\). Therefore the problem's
single final score is
\(\log_{10}(1/\mathrm{NRMSE})=7.096406336739107\). This agrees with the score
attribute above; the scoring rule has no additive components.

The numerical skeleton is exceptionally accurate. I reproduced the candidate's
all-training-row NRMSE \(8.494296887977806\times10^{-8}\) and Score
\(7.070872563858971\), and all held-out predictions were finite. The
candidate's table entry labelled “20,000-row holdout,” however, is the
fixed-seed 20,000-row partition of `train.csv` created by
`iteration2_fit.py`, not the designated held-out evaluation. Its reported
Score \(7.06574\) is internally reproducible but is not the final review score.

**CRITICAL — the dimensional-consistency claim is not supported under the
official variable descriptions.** The candidate obtains its dimensional
argument only by replacing the stated mechanical momentum with a magnetic
moment and by assuming both \(\alpha\) and \(f\) are dimensionless. A physical
polarizability is not generally dimensionless. Moreover,
\(1/(\epsilon c^2)\) has permeability units in SI, so multiplying it by
magnetization produces magnetic-flux-density units, not the units of the
\(H\)-field denoted by magnetic field strength. Thus neither the subtraction
nor \(\mathrm{mom}H/k_b\) has the claimed units under the official semantics.
The problem defines the score solely through held-out NRMSE and states no
separate dimensional penalty, so this critical scientific defect does not
alter the numeric score above.

The “zero fitted parameters” claim is also unsupported. The scripts explicitly
fit \(a_H\), \(a_M\), and \(p_c\), profile \(p_c\) over a grid, and then freeze
the data-selected values \(1,-1,2\). In the absence of an independent
theoretical derivation, these are three selected/model-fitting parameters, not
zero. The corrected count is still within the allowed maximum of four and
parameter count is not a score component. Apart from these two claim-level
issues, the metric implementation matches the stated NRMSE definition, the
reported ablations are consistent with the artifacts, and the train-to-held-out
accuracy supports the asserted numerical structure.
</review>
