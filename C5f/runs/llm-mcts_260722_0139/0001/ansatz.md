## One sentence

With the dimensionless radius \(q=r/R_0\), the proposed single expression is \(\displaystyle \widehat{\rho}_{\rm NFW/core}(r,R_0,x)=\frac{1+x}{2q(1+q)^2}+\frac{1-x}{2(1+q)(1+q^2)}\), with no fitted scalar constants.

## Motivation and explanation

The data collapse onto functions of \(q=r/R_0\). I first fit each \(x\) subset to the unconstrained factor family

$$
g(q)=\frac{A}{q^c(1+q)^a(1+q^2)^b}.
$$

Ordinary least squares on \(\log g\), with all four quantities free, gave

| Subset | \(A\) | \(c\) | \(a\) | \(b\) |
| --- | ---: | ---: | ---: | ---: |
| core, \(x=-1\) | \(0.9999999999999817\) | \(4.22\times10^{-15}\) | \(0.9999999999999778\) | \(1.000000000000003\) |
| NFW, \(x=1\) | \(0.9999999999999892\) | \(1.000000000000003\) | \(1.999999999999976\) | \(3.58\times10^{-15}\) |

The coefficients therefore reduce to exact small integers: \(g_+(q)=1/[q(1+q)^2]\) for the NFW subset and \(g_-(q)=1/[(1+q)(1+q^2)]\) for the core subset. Because the observed classes are exactly \(x=1\) and \(x=-1\), \((1+x)/2\) and \((1-x)/2\) are exact selectors. The result is one compact expression rather than two case statements.

The structure has the expected halo limits:

| Limit | NFW, \(x=1\) | core, \(x=-1\) |
| --- | --- | --- |
| \(q\to0\) | \(\widehat{\rho}\sim q^{-1}\), a cusp | \(\widehat{\rho}\to1\), a finite core |
| \(q\to\infty\) | \(\widehat{\rho}\sim q^{-3}\) | \(\widehat{\rho}\sim q^{-3}\) |

Both components are positive for \(q>0\), and their derivatives are

$$
g_+'(q)=-\frac{1+3q}{q^2(1+q)^3}<0,
\qquad
g_-'(q)=-\frac{1+2q+3q^2}{(1+q)^2(1+q^2)^2}<0.
$$

Thus the endpoint profiles are strictly decreasing. For any interpolated \(-1\le x\le1\), the ansatz is a convex combination of them and remains positive and strictly decreasing. Values between the two trained classes are not constrained by the dataset, so this affine selector is the simplest constraint-preserving interpolation; behavior for \(|x|>1\) is not claimed.

The expression is dimensionally consistent for the normalized target: \(r\) and \(R_0\) have the same length dimension, so \(q\), every factor, and both selector weights are dimensionless. If \(\rho\) is assigned physical density units rather than the dataset's normalization, the right-hand side must be multiplied by a reference density \(\rho_0\), fixed here to one in data units.

## Performance

Direct evaluation of the displayed dimensionless selector on all 20,000 rows gives

| Rows | MSE | RMSE | Maximum absolute error | Maximum relative error |
| --- | ---: | ---: | ---: | ---: |
| all 20,000 | \(6.207444566443756\times10^{-32}\) | \(2.491474376035956\times10^{-16}\) | \(6.217248937900877\times10^{-15}\) | \(8.082971043742636\times10^{-15}\) |
| core, \(x=-1\) | \(6.364546659284261\times10^{-33}\) | \(7.977810889764347\times10^{-17}\) | \(4.440892098500626\times10^{-16}\) | \(7.966325681806750\times10^{-15}\) |
| NFW, \(x=1\) | \(1.177843446695909\times10^{-31}\) | \(3.431972387266408\times10^{-16}\) | \(6.217248937900877\times10^{-15}\) | \(8.082971043742636\times10^{-15}\) |

These discrepancies are floating-point roundoff. Algebraically equivalent arithmetic forms gave MSE \(1.139570798089859\times10^{-31}\) for separated \(r,R_0\) terms and \(1.208236008489752\times10^{-31}\) for a single combined \(r,R_0\) fraction, so the displayed \(q\)-selector is also the best-conditioned tested evaluation.

Four fitting formulations were tested: log-space OLS, direct absolute residuals, direct relative residuals, and robust log residuals. All recovered the same integers within roughly \(10^{-13}\) or better. All 40 seeded nonlinear multistart fits converged to the same structure. The free log-linear design had condition number \(199.6\); nonlinear Jacobian condition numbers ranged from about \(169\) to \(328\), but changing the objective did not change the structural conclusion. Classical standard errors are at roughly \(10^{-15}\) and are not scientifically meaningful because the data are noiseless.

An exhaustive scan over integer \(c,a,b\in\{0,1,2,3\}\), refitting \(A\), selected the stated triples uniquely. The next-best direct-fit integer candidate had MSE \(9.11\times10^{-4}\) for the core subset and \(4.43\times10^{-3}\) for the NFW subset, compared with \(6.37\times10^{-33}\) and \(2.22\times10^{-31}\) for the selected structures. A block holdout of every fifth \(R_0\) grid value gave MSE \(2.54\times10^{-29}\) for core and \(7.26\times10^{-28}\) for NFW with the unrounded free-exponent fit, again at numerical precision.

Constraint diagnostics on \(10^{-8}\le q\le10^8\), far beyond the training interval \(0.0667\le q\le4\), verified positivity, strict monotonic decrease, the inner slopes \(0\) and \(-1\), and the shared outer slope \(-3\). SymPy independently verified both selector endpoints and the analytic derivatives.

## Difficulties, resolution, and open questions

The factor basis is moderately conditioned and its residuals are so small that correlations of residuals with inputs are dominated by floating-point arithmetic. I resolved that ambiguity by comparing residual objectives, random starts, integer structures, held-out \(R_0\) blocks, and algebraically equivalent evaluations. Every check supports the same exact rational expression.

The workspace had no usable project .venv. The system Python 3.13 interpreter was also unusable because its NumPy compiled extension could not import, so the working Python 3.12 environment was used; exact versions and the failure mode are recorded in [analysis_environment.md](analysis_environment.md). Ruff 0.12.5 was installed only inside this work directory.

The only substantive open question is how \(x\) should interpolate physically between the two observed classes: the data contain no intermediate \(x\). The proposed convex interpolation is simple and safe, but it is not empirically identifiable from this dataset. A dimensional density normalization is likewise implicit rather than learned.

## Artifacts

- [profile_models.py](profile_models.py) and [test_profile_models.py](test_profile_models.py): shared implementation and four unit tests.
- [iteration1_dimensionless_fit.py](iteration1_dimensionless_fit.py), [iteration1_coefficients.csv](iteration1_coefficients.csv), [iteration1_metrics.json](iteration1_metrics.json), [iteration1_report.txt](iteration1_report.txt), and [iteration1_diagnostics.png](iteration1_diagnostics.png): free dimensionless exponent discovery.
- [iteration2_structure_validation.py](iteration2_structure_validation.py), [iteration2_objective_fits.csv](iteration2_objective_fits.csv), [iteration2_multistart_sensitivity.csv](iteration2_multistart_sensitivity.csv), [iteration2_integer_scan_top.csv](iteration2_integer_scan_top.csv), [iteration2_R0_holdout.csv](iteration2_R0_holdout.csv), [iteration2_exact_metrics.json](iteration2_exact_metrics.json), [iteration2_report.txt](iteration2_report.txt), and [iteration2_diagnostics.png](iteration2_diagnostics.png): formulation, multistart, integer-structure, and holdout validation.
- [iteration3_combined_ansatz.py](iteration3_combined_ansatz.py), [iteration3_metrics.json](iteration3_metrics.json), [iteration3_worst_cases.csv](iteration3_worst_cases.csv), [iteration3_constraint_checks.csv](iteration3_constraint_checks.csv), [iteration3_report.txt](iteration3_report.txt), and [iteration3_parity_constraints.png](iteration3_parity_constraints.png): final full-data, worst-case, symbolic, asymptotic, interpolation, and parity diagnostics.
- [trend_r.png](trend_r.png) and [trend_R0.png](trend_R0.png): local rasterizations of the two problem-supplied trend PDFs used during inspection.
- [analysis_environment.md](analysis_environment.md) and .ruff_tool/: exact environment record, reproduction commands, and the locally installed Ruff 0.12.5 checker.

<review score="6.207444566443756e-32">
The candidate meets the requested single-expression form and reproduces the full dataset to binary64 roundoff. I independently loaded all 20,000 CSV rows and evaluated the displayed expression directly, without using stored predictions. With the documented default Pandas parsing and NumPy arithmetic, the full-data SSE is \(1.2414889132887512\times10^{-27}\), hence

\[
\mathrm{MSE}=\frac{1.2414889132887512\times10^{-27}}{20000}
=6.207444566443756\times10^{-32}.
\]

The component check agrees exactly: the 10,000 core rows have SSE \(6.364546659284261\times10^{-29}\) (MSE \(6.364546659284261\times10^{-33}\)), and the 10,000 NFW rows have SSE \(1.1778434466959086\times10^{-27}\) (MSE \(1.1778434466959087\times10^{-31}\)); summing those SSEs and dividing by 20,000 gives the stated total. The independently reproduced RMSE is \(2.491474376035956\times10^{-16}\), so the candidate has not confused MSE with RMSE. The maximum absolute and relative errors, \(6.217248937900877\times10^{-15}\) and \(8.082971043742636\times10^{-15}\), likewise match the report and show no model-scale residual pattern.

The structural checks are sound. Substitution of \(x=1\) and \(x=-1\) gives exactly \(1/[q(1+q)^2]\) and \(1/[(1+q)(1+q^2)]\), respectively. Symbolic differentiation confirms both derivatives printed in the candidate, and their positive-denominator/negative-numerator forms prove strict decrease for \(q>0\). The inner cusp/core limits and common \(q^{-3}\) outer limit follow directly. The affine selector is a convex combination only on \(-1\le x\le1\), and the candidate appropriately limits its claim to that interval and acknowledges that interpolation is not identifiable because the data contain only \(x=\pm1\).

There is no **CRITICAL** dimensional violation for the dataset as stated: \(q=r/R_0\) and \(x\) are dimensionless, and the target is supplied without physical units, so the expression consistently models a normalized density. If \(\rho\) is interpreted as a dimensional physical density, the printed right-hand side is instead \(\rho/\rho_0\) and requires the implicit density scale noted by the candidate; this is a physical-interpretation caveat, not a numerical scoring failure.

The phrase “no fitted scalar constants” is syntactically true of the frozen final formula but should not be read as parameter-free discovery. The workflow fit \((A,c,a,b)\) separately for both profiles and explicitly scanned integer \((c,a,b)\) triples. Thus two amplitudes and six exponents—including values later fixed to zero or one—are eight data-selected numerical/model-structure choices under the reviewer's hidden-parameter rule. The run has no ancestor or sibling candidates, so there is no additional cross-node selection evidence, but the within-node fitting and grid scan are explicit. Parameter count is not part of this problem's numeric rubric, so this caveat does not alter the MSE score.

At this accuracy, the last digits are implementation-dependent: reading the same decimal CSV with round-trip float parsing gives an algebraically equivalent evaluation MSE of \(1.9270672962973628\times10^{-33}\). This variation is entirely floating-point parsing/arithmetic noise; it does not indicate a different fit. Likewise, selecting the smallest roundoff MSE among equivalent arithmetic forms does not by itself establish that one form is formally “best-conditioned.” For a reproducible score, the value above uses the candidate's documented loader and direct displayed-form evaluation.

The rubric has one numeric component and no simplicity or parameter penalties. Therefore the final score is the full-data MSE, \(6.207444566443756\times10^{-32}\), consistent with the review attribute and the classwise component aggregation.
</review>
