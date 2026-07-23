# Pile efficiency ansatz discovery

## Objective

Discover an explicit symbolic ansatz for the pile efficiency
$\eta(h,N_r,N_c,R,C,S_p,D_r)$.

Pile efficiency $\eta$ is the ratio between:
- the lateral force experienced by a pile inside a pile group when it reaches 5 cm lateral displacement;
- the lateral force experienced by an identical single pile in the same soil under zero load eccentricity ($h=0$) at the same 5 cm displacement.

$\eta$ must be positive. In slightly less than half of the training data, $\eta>1$.

## Definitions

- The pile head is the ground-surface point where the pile emerges.
- Load eccentricity $h$ is the vertical distance between the lateral load application point and the pile head.
- The lateral capacity of a single pile is the lateral force, with $h=0$, required to produce 5 cm lateral displacement at the pile head.
- The lateral capacity of a pile group is defined analogously; the total group capacity is the sum of the capacities of all individual piles.
- Due to symmetry, the column number $C$ is measured from the nearest edge column.

## Variables

| Symbol | Unit | Meaning | Range |
| --- | --- | --- | --- |
| $h$ | m | load eccentricity | $0\sim\infty$ |
| $N_r$ | 1 | total number of rows | $1\sim5$ |
| $N_c$ | 1 | total number of columns | $1\sim5$ |
| $R$ | 1 | row number, counted from the leading row facing lateral load | $1\sim N_r$ |
| $C$ | 1 | column number, counted from the nearest edge column | $1\sim N_c/2$ |
| $S_p$ | 1 | pile spacing normalized by pile diameter | $1\sim\infty$ |
| $D_r$ | 1 | relative density of sand | $0<D_r<1$ |

## Data

Training data: `data/Train_2025409.csv`.

Reference document: `Regression.pdf`. Read it for the original regression context and pile-group geometry background.

The CSV has 224 rows and 8 columns:

| CSV column | Variable | Values |
| --- | --- | --- |
| `h` | $h$ | 1--10 |
| `Width` | $N_r$ | 1, 2, 3, 5 |
| `Length` | $N_c$ | 1, 2, 3, 5 |
| `RowPosition` | $R$ | 1, 2, 3, 4, 5 |
| `ColumnPosition` | $C$ | 1, 2, 3 |
| `Space_norm` | $S_p$ | 3, 5 |
| `Dr` | $D_r$ | 40, 65, 80; divide by 100 |
| `Eff` | $\eta$ | min 0.084, max 1.520, mean 0.640, median 0.654, std 0.324 |

The database is sparse, especially in $S_p$, which only has two observed values. Extrapolation in spacing should therefore rely on physical reasoning as well as fitting quality.

## Candidate requirements

The candidate must propose a fully explicit algebraic ansatz for $\eta(h,N_r,N_c,R,C,S_p,D_r)$ with tunable scalar coefficients.

For this problem, write fitting and analysis code to `<WORKDIR>/fit.py`. The script should:
- be runnable from the problem folder as `python <WORKDIR>/fit.py <WORKDIR>`;
- exit with an error if `<WORKDIR>` is not provided;
- read `data/Train_2025409.csv`;
- write all generated outputs only to `<WORKDIR>`;
- fit the ansatz coefficients;
- truncate final coefficients to two decimal places and report metrics before and after truncation;
- report the five worst absolute-error data points after truncation.

The final `ansatz.md` should include:
- the ansatz in LaTeX;
- fitted coefficient values before and after truncation;
- physical intuition behind the expression;
- how each hard constraint is satisfied;
- pre- and post-truncation metrics;
- generated artifacts, such as scripts, text outputs, or plots.

## Hard constraints

1. Spacing monotonicity: $\partial\eta/\partial S_p>0$.
2. Diminishing spacing effect: $\lim_{S_p\to\infty}\partial\eta/\partial S_p=0$. Prior literature reports that the marginal spacing effect is very small when $S_p>6$.
3. Single pile condition: for $N_r=N_c=R=C=1$ and $S_p=\infty$, $\eta$ must depend only on $h$, not on $D_r$; additionally, $\eta(h=0,N_r=1,N_c=1,R=1,C=1,S_p=\infty,D_r)=1$.
4. Load eccentricity: as $h$ increases, lateral efficiency decreases; $\lim_{h\to\infty}\eta=0$.
5. No free functions: the ansatz must contain only explicit algebraic expressions and fitted scalar coefficients.
6. Natural range coverage: with fitted coefficients in natural scenarios, the ansatz value range should cover the observed $\eta$ range in the database. For example, since the observed maximum is about 1.6, the formula must not impose a universal upper bound of 1.

## Scoring rubric

Higher is better.

For a dataset with residuals $e_i=\eta_{\mathrm{pred},i}-\eta_{\mathrm{obs},i}$, use:
$L_1=\frac{1}{n}\sum_i |e_i|$,
$L_2=\sqrt{\frac{1}{n}\sum_i e_i^2}$ (RMSE, not MSE),
and $L_\infty=\max_i |e_i|$.

1. Hard constraints: 10 points each, 60 points total.
2. Complexity penalty: subtract $0.5*LeafCount+5*max(0,N_{param}-4)$ from the score. This penalizes complex expressions and only penalizes fitted parameters beyond the first four. If a structural constant is chosen from a small discrete set and has plausible physical motivation, count it as 0.5 parameter. `LeafCount` means the minimum LeafCount among all equivalent expressions.
3. Loss and truncation-stability scores: for a loss $L$, baseline $L_0$, and base score $B$, use $B(\log_{10}(L_0/L)+1)$. Thus $L=L_0$ gives $B$, $L=10L_0$ gives 0, $L=100L_0$ gives $-B$, and $L=0.1L_0$ gives $2B$.

| Term | Quantity | Baseline | Base score | Cap |
| --- | --- | --- | --- | --- |
| Training L1 loss after truncation | $L_1^{train}$ | 0.04 | 10 | none |
| Validation L1 loss after truncation | $L_1^{vali}$ | 0.04 | 10 | none |
| Training L2 error after truncation | $L_2^{train}$ | 0.06 | 10 | none |
| Validation L2 error after truncation | $L_2^{vali}$ | 0.06 | 10 | none |
| Training max error after truncation | $L_\infty^{train}$ | 0.1 | 10 | none |
| Validation max error after truncation | $L_\infty^{vali}$ | 0.1 | 10 | none |
| Training L1 truncation stability | $r_{L1}$ | 10% | 10 | upper 10; if $r_{L1}\le0$, use 10 |
| Training L2 truncation stability | $r_{L2}$ | 10% | 10 | upper 10; if $r_{L2}\le0$, use 10 |

The reviewer should state every component score.
