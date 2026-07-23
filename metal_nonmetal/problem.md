# Metal/nonmetal descriptor discovery

## Objective

Discover a compact explicit symbolic descriptor pair $(d_1,d_2)$ for classifying 299 binary compounds as metal or nonmetal.

A binary compound $A_xB_{1-x}$ contains exactly two different elements. The descriptor should map each compound to a 2D plane where metals and nonmetals are well separated by a simple linear classifier.

## Data

Training data: `data/train.dat`.

The file has 299 compounds: the first 188 rows are metals and the last 111 rows are nonmetals. Labels are not stored as a column.

| Column | Meaning | Range |
| --- | --- | --- |
| `materials` | compound name | string |
| `IE_A` | first ionization energy of element A, eV | 3.893--10.43 |
| `IE_B` | first ionization energy of element B, eV | 5.786--17.42 |
| `X_A` | Pauling electronegativity of element A | 0.79--2.54 |
| `X_B` | Pauling electronegativity of element B | 1.61--3.98 |
| `xA` | atomic fraction of element A | 0.25--0.75 |
| `xB` | atomic fraction of element B | 0.25--0.75 |
| `Vcell_over_Vatom` | $V_{cell}/\sum V_{atom}$ | 0.27841--1.16904 |

You may also use `packing = 1 / Vcell_over_Vatom`, whose range is 0.8554--3.5918.

## Evaluation helper

Use `evaluation.py` for loading data, fitting scalar parameters, computing descriptors, evaluating train accuracy and LOOCV accuracy, and saving a descriptor plot.

Important functions:
- `load_data()` returns `(X, y, df)`, where metals have label `+1` and nonmetals have label `-1`.
- `fit_params(code, df, y)` is only a reference helper for fitting `params[i]`; you may use your own method to find the best parameters.
- `compute_descriptor(code, df, params)` returns `(d1, d2)`.
- `evaluate_pair(d1, d2, y)` returns `train_accuracy`, `loocv_accuracy`, and misclassified rows.
- `save_descriptor_plot(d1, d2, y, out_path)` saves a 2D metal/nonmetal scatter plot.

## Candidate requirements

The candidate must propose two explicit algebraic expressions $(d_1,d_2)$ using the available variables and optional fitted scalar parameters `params[0]`, `params[1]`, ... . Use at most 4 fitted parameters.

Before settling on the final descriptor:
- Consider every provided variable as potentially informative; if the final descriptor omits a variable, explain why.
- Brainstorm and test diverse formula families; do not only make small variants of the current best or simplest ionicity/packing descriptor.

Write the candidate in this format:

```
def descriptor(IE_A, IE_B, X_A, X_B, xA, xB, packing, params):
    ...
    return d1, d2
```

Use any analysis you need, but write all generated artifacts only to `<WORKDIR>`. Do not modify `evaluation.py`.

The final `ansatz.md` should include the descriptor formula, fitted parameters, physical intuition, train accuracy, LOOCV accuracy, misclassified rows, and generated artifacts.

## Scoring rubric

Higher is better.

The `<review score="...">` must be the LOOCV classification accuracy expressed as a percentage, using `LinearSVC` on $(d_1,d_2)$.

For example, if LOOCV accuracy is `0.9732`, write `<review score="97.32">`.

Use training accuracy, number of misclassified rows, expression simplicity, parameter count, and plot quality only as qualitative discussion or tie-breakers. Do not subtract them from the review score.
