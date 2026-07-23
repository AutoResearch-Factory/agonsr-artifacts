## Notes to ansatz-reviewer

The `<review score="...">` must be the LOOCV RMSE in eV, using linear regression on the candidate descriptor. Lower is better.

For example, if LOOCV RMSE is `0.1234` eV, write `<review score="0.1234">`.

Use full-fit RMSE/R², LOOCV R², expression simplicity, parameter count, physical interpretation, and plot quality only as qualitative discussion or tie-breakers. Do not subtract them from the review score.
