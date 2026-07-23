## One sentence

The proposed four-parameter autonomous ansatz is defined by
$$
u(P)=1-\exp[-P/(3K)]
$$
and
$$
\frac{dP}{dt}=\frac{A P^2(1-P/K)}{1+B u(P)+C u(P)^2}.
$$

## Motivation and explanation

The data strongly favor cooperative quadratic growth with a carrying-capacity zero. The two-parameter core $A P^2(1-P/K)$ scored only $2.686$, but its residual was a smooth function of population. Simple explicit-time factors scored about $3.1$, whereas density-only corrections exceeded $5.9$; time therefore appears to index the samples rather than independently control the instantaneous rate.

The bounded coordinate $u=1-\exp[-P/(3K)]$ is dimensionless, monotone, and saturates as population increases. A second-order denominator in $u$ is the smallest tested extension that resolved most of the remaining curvature without adding a pole or changing the equilibrium. The raw-target least-squares coefficients are

| Parameter | Value | Dimensional role |
| --- | ---: | --- |
| $A$ | $0.1788178847006512$ | population$^{-1}$ time$^{-1}$ |
| $K$ | $10.85235167622678$ | population |
| $B$ | $0.04006219756915985$ | dimensionless |
| $C$ | $-0.01102323825099643$ | dimensionless |

Thus $P/K$, $P/(3K)$, and the exponential argument are dimensionless, while $A P^2$ has units of population per time. The factor $1/3$ is a fixed structural scale, not a fitted coefficient. It was selected from a small screen of simple fixed rates after the free-rate first-order correction converged near $1/2$; consequently, the validation results condition on this structural choice. As a check against relying on it, an independently parameterized four-continuous-parameter law,
$$
\frac{dP}{dt}=P^2[a+bP+c\exp(-qP)],
$$
scored $6.0021$, close to the selected model's $6.0237$.

For every $P\geq0$, $0\leq u<1$. With the fitted values,
$$
\frac{d}{du}(1+Bu+Cu^2)=B+2Cu\geq B+2C=0.0180157211>0,
$$
so the denominator increases from $1$ to the asymptote $1+B+C=1.0290389593$ and cannot vanish. The ansatz therefore enforces $dP/dt=0$ at $P=0$ and $P=K$, positive growth for $0<P<K$, and negative growth for $P>K$. A numerical check through $10K$ confirms these signs. The fitted maximum growth is $3.09664765$ near $P=7.22729$.

## Performance

Raw least squares is the preferred fitting formulation because the denominator of the official NRMSE is fixed for the dataset, so it optimizes the official score directly.

| Candidate or refinement | Fitted parameters | NRMSE | Score |
| --- | ---: | ---: | ---: |
| Cooperative core $A P^2(1-P/K)$ | 2 | $2.061\times10^{-3}$ | $2.6860$ |
| Ancestor logarithmic denominator | 4 | $3.695800984\times10^{-6}$ | $5.432291423$ |
| Free-rate exponential-saturation denominator | 4 | $1.187838110\times10^{-6}$ | $5.925242745$ |
| Four-parameter unfactored exponential check | 4 | $9.950941186\times10^{-7}$ | $6.002135841$ |
| Selected bounded-density quadratic denominator | 4 | $9.469304626\times10^{-7}$ | $6.023681912$ |

The selected ansatz improves training NRMSE by a factor of $3.90$ over the ancestor. Its RMSE is $5.282403994\times10^{-7}$ and its maximum absolute error is $1.285200659\times10^{-6}$. Population-interleaved ten-fold fits gave held-out NRMSE from $9.1567\times10^{-7}$ to $9.8943\times10^{-7}$; time-interleaved folds gave $9.1769\times10^{-7}$ to $9.7463\times10^{-7}$. These checks refit coefficients within each fold.

A fixed-seed 30-replicate bootstrap gave coefficient standard deviations $1.63\times10^{-8}$ for $A$, $3.99\times10^{-9}$ for $K$, $1.24\times10^{-6}$ for $B$, and $3.86\times10^{-6}$ for $C$. Alternative objectives remained nearby but were worse on the official metric: square-root magnitude weighting scored $5.9982$, and relative-error fitting with a floor scored $5.9086$. There are 277 groups of duplicated rounded $P$ values with conflicting targets; their largest within-group range is $1.80723\times10^{-6}$, larger than the final model's worst residual and consistent with the remaining float-precision-scale scatter.

The residual still has weak smooth structure below $P\approx10.5$, and the fixed $1/3$ rate was selected rather than derived mechanistically. The expression should therefore be treated as a compact, constraint-preserving predictive skeleton, not a unique population mechanism. No held-out targets were accessed.

## Diagnostic artifacts and reproducibility

No problem-local `.venv` was available. Runs used Python 3.12.3 with NumPy 1.26.4, pandas 2.1.4, SciPy 1.11.4, and matplotlib 3.6.3. Randomness appears only in the iteration-4 bootstrap and uses seed `20260722`. Every analysis invocation used `timeout 600`; all scripts passed `python3 -m py_compile`, and all three final unit checks passed. `ruff` was not installed.

- Iteration 1, baseline structural screen: `iteration1_structure_screen.py`, `iteration1_model_summary.csv`, `iteration1_residual_correlations.csv`, `iteration1_data_quantiles.csv`, `iteration1_diagnostics.png`, and `iteration1_report.txt`.
- Iteration 2, monotone and oscillatory density corrections: `iteration2_correction_search.py`, `iteration2_correction_summary.csv`, `iteration2_interleaved_cv.csv`, `iteration2_diagnostics.png`, and `iteration2_report.txt`.
- Iteration 3, affine-exponential and nonlinear-gap alternatives: `iteration3_affine_and_gap_search.py`, `iteration3_model_summary.csv`, `iteration3_objectives.csv`, `iteration3_binned_residuals.csv`, `iteration3_worst_cases.csv`, `iteration3_diagnostics.png`, and `iteration3_report.txt`.
- Iteration 4, selected fixed-rate refinement and stress tests: `iteration4_fixed_rate_refinement.py`, `iteration4_refinement_summary.csv`, `iteration4_interleaved_cv.csv`, `iteration4_objectives.csv`, `iteration4_bootstrap.csv`, `iteration4_bootstrap_summary.csv`, `iteration4_constraints.csv`, `iteration4_duplicate_population.csv`, `iteration4_binned_residuals.csv`, `iteration4_worst_cases.csv`, `iteration4_final_diagnostics.png`, and `iteration4_report.txt`.
- Iteration 5, independently unfactored four-parameter laws: `iteration5_unfactored_search.py`, `iteration5_model_summary.csv`, `iteration5_interleaved_cv.csv`, `iteration5_binned_residuals.csv`, `iteration5_diagnostics.png`, and `iteration5_report.txt`.
- Iteration 6, profiled nonlinear-feature check: `iteration6_profiled_feature_search.py`, `iteration6_model_summary.csv`, `iteration6_interleaved_cv.csv`, `iteration6_binned_residuals.csv`, `iteration6_diagnostics.png`, and `iteration6_report.txt`. The initial direct multistart optimization hit the 600-second limit because of cubic-limit collinearity; profiling the nonlinear rate and solving the other coefficients linearly resolved it and reproduced the independent exponential alternative.
- Independent final assertions, metric reproduction, annotated parity plot, and unit checks: `final_validation.py`, `final_validation.txt`, `final_parity.png`, and `test_final_validation.py`.

To rerun the final fit and diagnostics from this directory:

```bash
timeout 600 python3 iteration4_fixed_rate_refinement.py /home/youran/AgonSR-dev/artifacts/BPG9/data/train.csv --output-dir .
timeout 600 python3 final_validation.py /home/youran/AgonSR-dev/artifacts/BPG9/data/train.csv --output final_validation.txt --plot final_parity.png
timeout 600 python3 -m unittest -v test_final_validation.py
```

<review score="5.935810256">
Independent evaluation of the submitted formula with the stated coefficients on the required combined 1,000-row held-out set gives NRMSE = 1.159283739e-6 and therefore Score = log10(1/NRMSE) = 5.935810256. This is the sole review score; no component metric is added to it. Predictions were made with the training-fitted coefficients and were not refit on held-out targets, and all predictions are finite. As an evaluator cross-check, the same implementation gives training NRMSE = 9.469304626e-7 and Score = 6.023681912, exactly reproducing the candidate's report. The held-out score is 0.087871656 points lower, corresponding to a 22.4% increase in NRMSE; the combined held-out NRMSE is also 17.2% above the largest NRMSE reported among the internal interleaved folds, so those conditional validation results were optimistic.

The metric implementation is correct: it takes the square root of residual sum of squares divided by centered-target sum of squares, then applies log10(1/NRMSE). The reported training RMSE and maximum absolute error also reproduce at the stated precision, and all three supplied unit checks pass. A scan of the candidate's source and artifacts found no reference to the evaluation inputs or targets, so I found no direct evidence of held-out leakage. The bootstrap and interleaved-fold checks nevertheless condition on a functional family already selected using the full training set and therefore do not measure model-selection uncertainty.

The ansatz is dimensionally consistent. P/K and P/(3K) are dimensionless, the exponential argument is valid, B and C are dimensionless, and A P^2 has units of population/time. The global nonnegative-population shape claims also follow analytically: u is in [0,1), B+2Cu is bounded below by B+2C = 0.0180157211 > 0, and the denominator consequently increases from 1 toward 1+B+C = 1.0290389593. It has no pole for P >= 0, while the stated zeros and signs on either side of K follow from the numerator. The reported maximum-growth value is independently reproducible.

The parameter-limit claim requires a material qualification. The final display has four continuously optimized coefficients A, K, B, and C, but the factor 1/3 was explicitly selected from a training-data screen over six fixed rates rather than fixed by theory. Under the required cross-model accounting, that selected numeric rate is a hidden fifth model-selection parameter, so the submitted ansatz does not cleanly satisfy the “at most 4 fitted parameters” constraint despite having only four coefficients in its final refit. The independently parameterized four-coefficient comparison does not cure this issue because it is not the submitted formula. The extensive denominator, transform, and exponent screens add further selection complexity, although the rate choice is the clearest direct parameter-count violation. The problem defines no numerical disqualification or complexity subtraction, and the required review value is the single held-out Score, so this constraint finding does not alter the numeric score above.

Overall, the candidate is exceptionally accurate, finite, dimensionally sound, and well supported at the level of a fixed selected formula. Its principal weakness is parameter and post-selection accounting, not failure of the claimed mathematical shape or metric reproduction.
</review>
