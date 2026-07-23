## One sentence

The proposed four-parameter autonomous ansatz is
$$
\frac{dP}{dt}=\frac{rP^2(1-P/K)}{1+a\log(1+qP/K)}.
$$

## Motivation and explanation

The dominant structure in the data is quadratic cooperative growth followed by density saturation: a direct polynomial screen strongly selected the terms $P^2$ and $P^3$, which combine as $rP^2(1-P/K)$. Standard logistic, Gompertz, Richards, beta-gap, and cooperative birth-minus-loss laws were substantially less accurate. A small, smooth residual remained across the population range; the compact positive denominator $1+a\log(1+qP/K)$ captured that curvature better than polynomial, exponential, power-law, and rational alternatives under the four-parameter limit.

The fitted coefficients, using raw-target least squares, are

| Parameter | Value | Dimensional role |
| --- | ---: | --- |
| $r$ | $0.17882864524021$ | population$^{-1}$ time$^{-1}$ |
| $K$ | $10.852351774337$ | population |
| $a$ | $0.020249657331206$ | dimensionless |
| $q$ | $0.68346019028964$ | dimensionless |

Thus $P/K$ and the logarithm argument are dimensionless, while both sides have units of population per time. The expression enforces $dP/dt=0$ at $P=0$ and $P=K$. Its fitted denominator is positive for every $P\geq0$, so growth is positive on $0<P<K$ and negative for $P>K$ without a nonphysical pole. On a dense check over $0\leq P\leq2K$, both sign conditions held; the fitted maximum growth is $3.09665747$ at $P=7.22766628$.

Time $t$ does not appear explicitly. The target is already almost single-valued in $P$, and tested time-dependent logistic, Richards, sinusoidal, and exponential corrections were markedly worse. The interpretation is therefore an autonomous population law in which $t$ indexes the observed trajectory rather than independently controls the instantaneous rate.

## Performance

The official metric was optimized directly. Since its denominator is fixed for the data, raw least squares minimizes NRMSE exactly.

| Candidate/refinement | Parameters | NRMSE | Score |
| --- | ---: | ---: | ---: |
| Standard logistic $c_1P+c_2P^2$ | 2 | $4.99419\times10^{-1}$ | $0.3015$ |
| Quadratic-contact law $rP^2(1-P/K)$ | 2 | $2.061\times10^{-3}$ | $2.6860$ |
| Generalized two-power saturation | 4 | $2.672\times10^{-5}$ | $4.5731$ |
| Quadratic rational correction | 4 | $5.146\times10^{-6}$ | $5.2885$ |
| Final logarithmic-denominator ansatz | 4 | $3.695800984\times10^{-6}$ | $5.432291423$ |

For the final ansatz, RMSE is $2.061684004\times10^{-6}$ and the maximum absolute training error is $9.943486614\times10^{-6}$. The largest errors occur near the growth maximum, around $P=7.3$--$7.9$; near the densely sampled equilibrium region, population-bin RMSE is typically $5$--$7\times10^{-7}$.

Population-stratified five-fold fits gave held-out NRMSE from $3.6801\times10^{-6}$ to $3.7264\times10^{-6}$ and maximum held-out absolute error below $9.95\times10^{-6}$. A fixed-seed 30-replicate bootstrap gave standard deviations $1.88\times10^{-7}$ for $r$, $5.90\times10^{-9}$ for $K$, $2.03\times10^{-5}$ for $a$, and $9.33\times10^{-4}$ for $q$.

Alternative fitting formulations exposed the expected tradeoff. Robust soft-$L_1$ fitting retained NRMSE $3.762\times10^{-6}$ and nearby coefficients; fitting $(dP/dt)/P^2$ emphasized low populations but worsened official NRMSE to $1.116\times10^{-5}$. Population-quantile balancing reproduced the raw optimum. The raw objective is preferred because it matches the official score, has stable coefficients, and does not sacrifice any population region under the observed sampling.

There is a small irreducible/data-precision component: 277 rounded $P$ values occur more than once and every such group has slightly conflicting targets, with a maximum within-group range of $1.81\times10^{-6}$. The remaining residual also retains smooth bias at low and intermediate $P$, so the ansatz should be treated as the best supported compact skeleton, not proof of a unique microscopic mechanism. The near-tied binomial denominator $rP^2(1-P/K)/(1+qP/K)^m$ scores $5.4223$, only $0.0100$ below the selected form; measurements below $P=1$, more independent samples through the transition region, or mechanistic prior information would help distinguish them.

## Reproducibility and artifacts

No problem-local `.venv` was available, so the scripts used Python 3.12.3 with NumPy 1.26.4, pandas 2.1.4, SciPy 1.11.4, and matplotlib 3.6.3. Every run was deterministic and invoked with `timeout 600`; bootstrap randomness uses seed `20260722`. All scripts passed `python3 -m py_compile`.

- Iteration 1 baseline code and diagnostics: `iteration1_baselines.py`, `iteration1_summary.csv`, `iteration1_residual_correlations.csv`, `iteration1_data_quantiles.csv`, `iteration1_diagnostics.png`, and `iteration1_report.txt`.
- Iteration 2 density-law refinement: `iteration2_density_law.py`, `iteration2_summary.csv`, `iteration2_conditioning.csv`, `iteration2_fivefold.csv`, `iteration2_residual_correlations.csv`, `iteration2_diagnostics.png`, and `iteration2_report.txt`.
- Iteration 3 model-family comparison: `iteration3_model_search.py`, `iteration3_summary.csv`, `iteration3_polynomial_screen.csv`, `iteration3_binned_residuals.csv`, `iteration3_worst_cases.csv`, `iteration3_diagnostics.png`, and `iteration3_report.txt`.
- Iteration 4 final fitting and stress tests: `iteration4_shape_validation.py`, `iteration4_summary.csv`, `iteration4_objectives.csv`, `iteration4_fivefold.csv`, `iteration4_bootstrap.csv`, `iteration4_bootstrap_summary.csv`, `iteration4_constraints.csv`, `iteration4_data_diagnostics.csv`, `iteration4_duplicate_P.csv`, `iteration4_binned_residuals.csv`, `iteration4_worst_cases.csv`, `iteration4_final_diagnostics.png`, and `iteration4_report.txt`.

To reproduce the final pass from this directory:

```bash
timeout 600 python3 iteration4_shape_validation.py /home/youran/AgonSR-dev/artifacts/BPG9/data/train.csv --output-dir .
```

<review score="5.390995366">
Independent evaluation of the submitted formula and the stated coefficients on the required concatenated 1,000-row held-out set gives NRMSE = 4.064476660e-6 and therefore Score = -log10(NRMSE) = 5.390995366. This is the sole review score. As a cross-check on the evaluator, the same implementation gives training NRMSE = 3.695800984e-6 and Score = 5.432291423, reproducing the candidate's reported values. The held-out score is 0.041296057 points below the training score, a modest but real generalization gap; the held-out NRMSE is also about 9% above the upper end of the reported internal five-fold range, so that validation was mildly optimistic.

The metric implementation is correct: it uses the square root of residual sum of squares divided by centered-target sum of squares, followed by log10(1/NRMSE), rather than confusing this quantity with MSE or unnormalized L2 error. Predictions were made with the submitted training-fitted coefficients and were not refit on held-out targets. All held-out predictions and logarithms are finite. I found no references to held-out paths in the candidate scripts or artifacts, so there is no direct evidence of test leakage.

The expression is dimensionally consistent. P/K and qP/K are dimensionless, the logarithm therefore has a valid dimensionless argument, and rP^2 has units of population/time. With the submitted positive a and q, the denominator is at least one for P >= 0; hence there is no nonnegative-population pole, and the stated zeros and sign change at K follow analytically rather than only from the dense-grid check.

The displayed formula has exactly four continuously fitted coefficients (r, K, a, q), satisfying the literal parameter count. However, the stronger claim that the search itself used only four degrees of freedom needs qualification. The artifacts explicitly screened polynomial powers, first fitted alpha and nu, and then fixed the population and saturation exponents to 2 and 1 before spending the released coefficient slots on a selected correction family. In particular, the motivation says the quadratic power was selected by a polynomial screen rather than derived independently. Under cross-candidate parameter-accounting rules, these are data-selected discrete structural hyperparameters (albeit weaker than continuous fitted parameters), and selection of the logarithmic denominator from many tested transforms adds further model-selection optimism. Thus “four-parameter” is accurate only for the final continuous refit, not for total search complexity. The problem specifies no numerical complexity penalty, and the required score is the held-out metric itself, so this caveat does not alter the score above.

Overall, the numerical claims are unusually well supported and independently generalize at nearly the reported accuracy. The principal evidence limitation is not predictive failure but post-selection accounting: bootstrap and five-fold results condition on the already selected functional family and therefore do not quantify uncertainty from the extensive family/power search.
</review>
