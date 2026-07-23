## One sentence

For positive inputs on the sub-resonant branch, with $P=\mathrm{Pwr}$, the proposed parameter-free ansatz is

$$
\boxed{\omega=\frac{\omega_0}{\sqrt{1+\sqrt{\frac{4\pi\epsilon cE_f^2r^2}{3P}}}}}.
$$

## Motivation and explanation

The inputs match the driven-dipole scattering law. The incident intensity and frequency-dependent scattering cross section are

$$
I=\frac{\epsilon cE_f^2}{2},
\sigma=\frac{8\pi r^2}{3}\frac{\omega^4}{(\omega_0^2-\omega^2)^2},
$$

so their product gives

$$
P=\frac{4\pi}{3}\epsilon cE_f^2r^2
\frac{\omega^4}{(\omega_0^2-\omega^2)^2}.
$$

Every one of the 80,000 observations has $0<\omega<\omega_0$. On this branch, define the dimensionless quantity

$$
q=\sqrt{\frac{3P}{4\pi\epsilon cE_f^2r^2}}
=\frac{\omega^2}{\omega_0^2-\omega^2}.
$$

Solving gives $\omega=\omega_0\sqrt{q/(1+q)}$, which is algebraically the boxed expression. The coefficient $4\pi/3$ follows from the intensity and dipole cross section, so it is a physical constant in this model rather than a fitted parameter.

The formula is dimensionally consistent: $\epsilon E_f^2$ is an energy density, hence $\epsilon cE_f^2r^2$ has units of power, and the nested-radical argument is dimensionless. It also satisfies the important constraints by construction:

- $0<\omega<\omega_0$ for all positive finite inputs.
- As $P\to0^+$,
  
  $$
  \omega\sim\omega_0(\frac{3P}{4\pi\epsilon cE_f^2r^2})^{1/4}.
  $$
- As $P\to\infty$, $\omega\to\omega_0^-$.
- It is strictly increasing in $P$ and $\omega_0$, and strictly decreasing in $\epsilon$, $c$, $|E_f|$, and $r$ on the positive domain.

The super-resonant branch is genuinely ambiguous from scattered power alone because the forward law contains $(\omega_0^2-\omega^2)^2$. When $q>1$, that alternative is $\omega=\omega_0\sqrt{q/(q-1)}$. The data select only the sub-resonant branch, so the boxed expression should not be extrapolated to a future dataset that mixes branches without an additional branch indicator.

## Ansatz refinement and fitting formulations

All fitted comparisons used a deterministic 80/20 split (seed 32117): 64,000 rows for fitting and 16,000 for holdout evaluation. Metrics were computed in float64 using the problem definition.

### Iteration 1: dimensionally valid power law

I first tested

$$
\frac{\omega}{\omega_0}=A(\frac{P}{\epsilon cE_f^2r^2})^b,
$$

using direct-frequency least squares, log-ratio OLS, and robust relative error. Direct-frequency fitting was best, with $A=0.5720793$, $b=0.1380219$, holdout NRMSE $0.112172$, all-data NRMSE $0.112536$, and score $0.948707$. The residual was strongly U-shaped against dimensionless power. This candidate captures the $P^{1/4}$ low-power idea only locally and cannot represent saturation at $\omega_0$.

### Iteration 2: resonance-aware one-parameter law

I revised the candidate to

$$
\frac{\omega}{\omega_0}=(1+\sqrt{\frac{K\epsilon cE_f^2r^2}{P}})^{-1/2}.
$$

Six formulations estimated $K$: direct frequency, log frequency, robust relative frequency, direct forward power, and the mean or median of the rearranged log-invariant

$$
K_i=\frac{P_i}{\epsilon_i c_iE_{f,i}^2r_i^2}
\frac{(\omega_{0,i}^2-\omega_i^2)^2}{\omega_i^4}.
$$

Their estimates ranged from $4.1887901993$ to $4.1887902190$; $4\pi/3=4.1887902048$ lies inside that $2.0\times10^{-8}$ spread. The median-invariant estimate had the smallest holdout NRMSE, $1.816393\times10^{-7}$, while direct-frequency fitting had all-data NRMSE $1.814177\times10^{-7}$. Forward-power least squares was slightly worse because large powers receive disproportionate leverage. The close agreement among differently conditioned objectives indicates that the coefficient and functional form are identified, not an artifact of one loss transformation.

### Iteration 3: four-parameter challenge and reduction

To test rather than assume the radicals, I fitted the maximum-allowed four-parameter generalization

$$
\frac{\omega}{\omega_0}=A[1+(\frac{K\epsilon cE_f^2r^2}{P})^p]^{-q}.
$$

Direct-frequency least squares recovered

$$
A=0.9999999923,K=4.1887903130,
p=0.5000000119,q=0.4999999838.
$$

Log-frequency and robust-relative fits likewise recovered $A=1$, $K=4\pi/3$, and $p=q=1/2$ to sub-ppm precision. Twelve deterministic 10,000-row subsample refits deviated from the theoretical values by at most $0.20$ ppm. The flexible direct fit had Jacobian condition number $536$ and improved holdout NRMSE over fixed theory by only $6.0\times10^{-12}$ in absolute terms, consistent with fitting float32 rounding. The zero-parameter physical reduction is therefore preferred.

## Performance

The final expression uses no fitted parameters and satisfies the four-parameter limit. On all 80,000 rows:

| Quantity | Result |
| --- | ---: |
| NRMSE | $1.8141908\times10^{-7}$ |
| Score | $6.7413170$ |
| Mean residual | $-3.43\times10^{-10}$ |
| Maximum absolute residual | $4.319\times10^{-7}$ |
| Maximum observed forward-power relative error | $1.456\times10^{-6}$ |

The mean residual in each of ten equal-count $\omega/\omega_0$ bins stays within $2.20\times10^{-9}$ of zero. The residual RMS rises smoothly from $7.37\times10^{-8}$ in the lowest-ratio bin to $1.17\times10^{-7}$ nearest resonance, as expected when float32 input and target quantization are propagated. No structured bias remains at a scale material to the score.

Equivalent float64 reciprocal, $q/(1+q)$, and stable-log implementations differ by at most $1.33\times10^{-15}$ and have the same reported NRMSE. Re-evaluating in float32 worsens NRMSE to $2.61\times10^{-7}$–$2.70\times10^{-7}$; float64 should therefore be used. For extreme positive inputs, a stable implementation can set

$$
x=\frac{P}{\epsilon cE_f^2r^2},
\log\frac{\omega}{\omega_0}=-\frac12\operatorname{logaddexp}
(0,\frac12[\log(4\pi/3)-\log x]).
$$

On a synthetic grid spanning $10^{-24}\le x\le10^{24}$, this implementation remained strictly increasing and strictly between zero and one. The analytic elasticities over the observed data are $0.0544$ to $0.2462$ for $P$, the negatives of those values for $\epsilon$ and $c$, twice those magnitudes for $E_f$ and $r$, and exactly $1$ for $\omega_0$. A $0.1\%$ perturbation of $4\pi/3$ raises NRMSE to about $6.20\times10^{-4}$, further confirming that the theoretical coefficient is sharply resolved.

## Reproducibility and validation

The problem workspace had no executable `.venv`, so the scripts used Python 3.12.3 with NumPy 1.26.4, pandas 2.1.4+dfsg, SciPy 1.11.4, and Matplotlib 3.6.3. Every analysis run was invoked through `timeout 600`. Ruff 0.12.7 reports no violations, and `python3 -m pytest -q test_models.py` reports four passing tests covering forward/inverse recovery, algebraic equivalence, constraints, monotonicity, and deterministic splitting. No randomness is used except the exposed fixed split/subsample seed 32117.

## Artifacts

- `model_utils.py`: validated loading, forward/inverse physical laws, metric definitions, and deterministic splitting.
- `iteration1_powerlaw.py`, `iteration1_metrics.csv`, `iteration1_diagnostics.png`: low-power candidate, three fitting objectives, parity plot, and structured residuals.
- `iteration2_resonance.py`, `iteration2_metrics.csv`, `iteration2_diagnostics.png`: six one-parameter formulations, coefficient-invariant distribution, parity, and residuals.
- `iteration3_generalized.py`, `iteration3_metrics.csv`, `iteration3_stability.csv`, `iteration3_diagnostics.png`: four-parameter challenge, conditioning, deterministic subsample stability, and comparison with fixed theory.
- `final_diagnostics.py`, `final_metrics.csv`, `final_summary.json`: equivalent numerical forms, environment, aggregate performance, and constraint checks.
- `final_diagnostics.png`: final annotated parity plot, residuals, dimensionless collapse, hard bound, and analytic sensitivity.
- `final_worst_cases.csv`, `final_binned_residuals.csv`, `final_sensitivity.csv`, `final_coefficient_sensitivity.csv`: worst rows, residual bins, elasticities, and coefficient perturbations.
- `test_models.py`: four reproducible unit tests.

## Closing notes

I used dimensional analysis and the driven-dipole law to turn an initially inadequate power law into a resonance-aware inverse, tested that inverse under multiple objectives, challenged its fixed exponents with the full parameter budget, and then reduced it to the simpler zero-parameter expression. The main difficulty was distinguishing a genuine coefficient fit from float32 rounding and objective-dependent weighting; invariant rearrangements, a holdout split, subsample refits, forward-law checks, and equivalent numerical implementations resolved that issue. The remaining open question is branch selection outside the supplied data: scattered power alone cannot distinguish sub-resonant and super-resonant solutions where both exist.

<review score="6.7450395938272685">
The boxed ansatz passes the substantive checks. Its derivation is algebraically correct on the stated sub-resonant branch: substituting the quoted intensity and scattering cross section gives the stated power law, and inversion yields exactly the boxed expression. It is dimensionally consistent because $\epsilon E_f^2$ is an energy density, so $\epsilon cE_f^2r^2/P$ is dimensionless and the result has the frequency units of $\omega_0$. The positivity, upper-bound, limiting, and monotonicity claims follow directly from the formula. The branch limitation is real and is disclosed appropriately rather than hidden.

The zero-parameter count is defensible. The only nontrivial numeric constant, $4\pi/3$, follows exactly from the displayed physical intensity and dipole-cross-section coefficients. The run has no ancestor or sibling candidates from which a tuned hard-coded constant could have been selected. The exploratory one- and four-parameter fits corroborate the theoretical reduction but are not part of the submitted predictor; even a conservative count treating the coefficient as fitted would remain below the four-parameter cap.

I independently evaluated the exact boxed expression in float64 and cross-checked it against an algebraically equivalent log-stable implementation. The held-out NRMSE is $1.7987069228593278\times10^{-7}$; the two implementations differ only at floating-point roundoff. Therefore the single final score defined by the problem is
$$
\log_{10}(1/\mathrm{NRMSE})=-\log_{10}(1.7987069228593278\times10^{-7})=6.7450395938272685.
$$
The candidate's reported training-set NRMSE and score are reproducible under the problem's metric, but that training score is not used as the review score. There are no additive score components in this problem: NRMSE is the intermediate diagnostic and $6.7450395938272685$ is the final score.

No critical constraint violation, scoring error, leakage into the submitted parameter-free formula, or material unsupported performance claim was found. The included tests pass; the main caveat remains the explicitly acknowledged non-identifiability of the resonance branch when extrapolating beyond the stated domain.
</review>
