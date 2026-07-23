## One sentence

The proposed zero-parameter ansatz is
$$
\boxed{x_1=x_2\cos(\theta_1-\theta_2)-\sqrt{x^2-x_2^2\sin^2(\theta_1-\theta_2)}}.
$$

## Motivation and explanation

Represent the two planar vectors as $\boldsymbol r_1=x_1(\cos\theta_1,\sin\theta_1)$ and $\boldsymbol r_2=x_2(\cos\theta_2,\sin\theta_2)$. Let the endpoint separation be $x=\lVert\boldsymbol r_1-\boldsymbol r_2\rVert$. The law of cosines gives the invariant
$$
x^2=x_1^2+x_2^2-2x_1x_2\cos(\theta_1-\theta_2).
$$
Solving this quadratic for $x_1$ gives
$$
x_1=x_2\cos(\theta_1-\theta_2)
\pm\sqrt{x^2-x_2^2\sin^2(\theta_1-\theta_2)}.
$$
Every one of the 64,888 supplied rows is closer to the minus root than to the plus root, so the ansatz uses the minus branch.

This expression has several structural advantages:

- It has no fitted parameters, below the allowed maximum of four.
- It is invariant under a common rotation of both vectors because it depends only on $\theta_1-\theta_2$.
- It satisfies the geometric quadratic constraint by construction.
- Its domain condition, $x^2\ge x_2^2\sin^2(\theta_1-\theta_2)$, is the condition for a real intersection; every training row satisfies it.
- It is dimensionally consistent. The angles are dimensionless, $x$, $x_1$, and $x_2$ have the same length unit, the radicand has units of length squared, and both terms on the right have units of length.

The official description calls $x_1$ a magnitude, but 58,289 rows (89.83%) have $x_1<0$. The data therefore encode a signed radial coordinate/root rather than a conventional nonnegative magnitude. Taking an absolute value or selecting the upper root strongly disagrees with the data.

## Search and fitting iterations

### Iteration 1: candidate geometry and branch selection

Five candidates were evaluated on all data and on a deterministic 80/20 split. The lower quadratic root achieved full-data NRMSE $1.9465\times10^{-7}$ and score $6.71074$. In contrast, the projection-minus-distance approximation scored $0.674$, the upper root scored $-0.530$, and a positive-distance interpretation scored $-0.544$. Replacing the angle difference by an angle sum was not even real-valued on 4,065 rows and scored $-0.076$ on its valid subset. The geometric radicand was nonnegative for every row.

### Iteration 2: relaxed coefficients and multiple fitting objectives

To test whether the unit coefficients were merely assumed, I fitted the relaxed invariant
$$
x^2=A x_1^2+B x_2^2+C x_1x_2\cos(k(\theta_1-\theta_2)).
$$
Raw algebraic least squares, scale-normalized least squares, normalized Huber loss, a four-parameter nonlinear invariant fit, and a direct-root soft-$L_1$ fit were compared on the same deterministic holdout. Representative results are:

| Formulation | $A$ | $B$ | $C$ | $k$ | Holdout score |
| --- | ---: | ---: | ---: | ---: | ---: |
| Raw algebraic OLS, $k=1$ | 0.9999999994 | 0.9999999994 | -1.9999999981 | 1 | 6.88743 |
| Normalized algebraic OLS, $k=1$ | 1.0000000002 | 0.9999999995 | -2.0000000014 | 1 | 6.88724 |
| Normalized invariant, $k$ fitted | 1.0000000011 | 0.9999999997 | -2.0000000017 | 1.0000000013 | 6.88642 |
| Direct root soft-$L_1$, $k$ fitted | 0.9999999989 | 0.9999999891 | -1.9999999960 | 0.9999999968 | 6.88557 |
| Theory-fixed, no fitted parameters | 1 | 1 | -2 | 1 | **6.88751** |

Normalization reduced the design-matrix condition number from 4.98 to 2.92, but did not improve holdout accuracy. The raw-fit formal standard errors for $(A,B,C)$ were $(6.06\times10^{-10},1.92\times10^{-9},1.75\times10^{-9})$, and the theoretical coefficients were all within $1.1$ formal standard errors. All objectives recover the exact geometric coefficients, while the theory-fixed expression slightly outperforms every fitted variant on holdout. The fitted deviations are therefore best interpreted as float32 rounding noise, not additional physics.

### Iteration 3: numerical, constraint, and robustness validation

The final expression was evaluated in direct float64, cancellation-resistant float64, and direct float32 forms. The cancellation-resistant form uses the algebraically equivalent identity
$$
x_1=\frac{(x_2-x)(x_2+x)}
{x_2\cos(\theta_1-\theta_2)+\sqrt{x^2-x_2^2\sin^2(\theta_1-\theta_2)}}
$$
when the direct subtraction is prone to cancellation, and otherwise uses the boxed expression. This is an implementation detail, not a different ansatz.

The direct and stable float64 implementations differ by at most $1.27\times10^{-14}$ on these data. Direct float32 evaluation is worse, with score $6.64229$, so float64 evaluation is preferred. Twenty deterministic random 20% subsets gave scores from $6.45216$ to $6.91753$; the range is driven by whether the rare near-tangent worst case is included. Adding independent relative input perturbations of $10^{-7}$ produced a median prediction change of $4.65\times10^{-7}$ and a 95th percentile of $1.69\times10^{-6}$. All tested perturbations through $10^{-5}$ retained a nonnegative radicand.

## Performance

The final cancellation-resistant float64 implementation on all 64,888 rows gives:

| Quantity | Result |
| --- | ---: |
| Fitted parameters | 0 |
| RMSE | $6.48854\times10^{-7}$ |
| MAE | $2.72743\times10^{-7}$ |
| Maximum absolute error | $1.23696\times10^{-4}$ |
| NRMSE | $1.94654\times10^{-7}$ |
| Official score | **6.710737651** |
| Rows selecting the lower branch | 64,888 / 64,888 |
| Minimum radicand | $9.75913\times10^{-5}$ |
| Normalized invariant RMSE | $4.62314\times10^{-8}$ |

The largest residual occurs at the smallest radicand, where the square root is most sensitive to independently rounded float32 inputs. Negative-target rows score $6.845$ as a slice, while the smaller nonnegative subset scores $5.780$ because it contains this near-tangent outlier. There is no systematic model-scale residual pattern away from the boundary.

## Difficulties and open questions

The main conceptual difficulty was the conflict between the word “magnitude” and the predominantly negative target. Explicit comparison of both quadratic roots resolves it empirically, but the reason the benchmark labels this signed branch a magnitude is not documented. The other limitation is irreducible boundary sensitivity: when the radicand is small, float32 rounding of the inputs is amplified by the square root. A numerically stable evaluation reduces arithmetic cancellation but cannot reconstruct the unrounded latent inputs.

The problem workspace had no `.venv`, so the analyses used the available Python 3.12.3 environment with NumPy 1.26.4, pandas 2.1.4, SciPy 1.11.4, and Matplotlib 3.6.3. Ruff was not installed, so it could not be run without introducing an unavailable dependency; all files passed `py_compile` and four focused unit tests.

## Artifacts

- `model_utils.py`: validated data loading, geometric roots, stable evaluation, and official metrics.
- `test_model_utils.py`: four unit tests covering both roots, cancellation, invalid geometry, and the official metric.
- `iteration1_candidate_survey.py`: first candidate and branch survey.
- `iteration1_candidate_metrics.csv`, `iteration1_data_summary.csv`, and `iteration1_geometric_checks.csv`: first-pass numerical results.
- `iteration1_candidate_diagnostics.png`: candidate scores, residual distribution, and boundary behavior.
- `iteration2_fit_variants.py`: relaxed-model fitting under multiple objectives.
- `iteration2_fit_results.csv` and `iteration2_coefficient_uncertainty.csv`: coefficients, conditioning, holdout metrics, and formal uncertainties.
- `iteration2_fit_diagnostics.png`: coefficient-recovery and holdout-score comparison.
- `iteration3_validation.py`: final precision, slice, split, perturbation, constraint, and worst-case validation.
- `iteration3_implementation_metrics.csv`, `iteration3_slice_metrics.csv`, `iteration3_split_stability.csv`, `iteration3_sensitivity.csv`, `iteration3_constraint_checks.csv`, and `iteration3_worst_cases.csv`: final diagnostic tables.
- `iteration3_final_diagnostics.png`: annotated parity plot, residuals, and numerical-boundary plot.

Reproduce the analyses from this directory with:

```bash
timeout 600 python3 -m unittest -v test_model_utils.py
timeout 600 python3 iteration1_candidate_survey.py
timeout 600 python3 iteration2_fit_variants.py
timeout 600 python3 iteration3_validation.py
```

<review score="6.911924084">
The single final held-out evaluation gives NRMSE \(1.22483028512\times10^{-7}\), hence
\[
\mathrm{Score}=\log_{10}(1/\mathrm{NRMSE})=6.91192408382,
\]
reported as \(6.911924084\). Independent vectorized and scalar evaluations agree at this precision, and the direct boxed expression and its cancellation-resistant algebraic implementation give the same reported score. This problem has no additive score components, so this transformed NRMSE is the complete review score. The score shown earlier in the candidate body is a training-set diagnostic, not the final review score.

The derivation is correct: expanding \(\lVert\boldsymbol r_1-\boldsymbol r_2\rVert^2\) produces the stated quadratic in \(x_1\), and applying the quadratic formula produces exactly the two displayed roots. The supplied training data independently reproduce the candidate's reported NRMSE, contain no invalid radicands, and select the lower root throughout. The held-out score confirms that this branch choice generalizes.

Dimensional consistency passes. The trigonometric arguments are dimensionless; \(x^2\) and \(x_2^2\sin^2(\theta_1-\theta_2)\) both have units of length squared; and both terms in the predicted \(x_1\) have units of length. There is therefore no critical dimensional violation.

The coefficients and exponents in the boxed formula follow from the exact geometric identity rather than a numerical fit, so zero continuous fitted parameters is supported. The minus sign was selected empirically from the two algebraic branches and is best regarded as one discrete model-selection choice rather than a theoretically forced sign; even under that conservative accounting, the candidate remains well within the limit of four fitted parameters. The thresholds used only to switch between algebraically equivalent floating-point evaluations are numerical safeguards, not model parameters.

The evidence package is internally consistent: the official NRMSE implementation matches the problem definition, all four focused unit tests pass, the relaxed fits recover the theoretical coefficients to numerical precision, and no held-out-data reference appears in the candidate's source or artifacts. The main caveat is semantic rather than predictive: the selected lower root can be negative, so it is not a conventional vector magnitude despite the official wording. The candidate clearly discloses this mismatch and models the encoded target correctly. Near-tangent cases remain sensitive to rounded inputs, but the stable form addresses avoidable cancellation without changing the ansatz.
</review>
