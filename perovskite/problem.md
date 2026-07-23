# Perovskite ABX3 stability classification

## Problem Statement

Perovskite is a specific crystal structure with the general formula ABX3, where A and B are two different cations (typically rA > rB) and X is an anion (one of oxygen, fluorine, chlorine, bromine, or iodine).
In the ideal perovskite structure the smaller B cation sits at the centre of a BX6 octahedron formed by six corner-sharing X anions, while the larger A cation fills the cavity between the octahedral framework.
Perovskite compounds are used in photovoltaics, optoelectronic devices, catalysts, and solid-state electrolytes; predicting before synthesis whether a given (A, B, X) combination actually forms a stable perovskite structure is therefore a classical materials-screening problem, and stability is primarily governed by the sizes (Shannon ionic radii rA, rB, rX in angstrom) and oxidation states (nA, nB, nX) of the three ions.
The Goldschmidt tolerance factor, proposed in 1926, is the earliest quantitative criterion for this task and is still in widespread use, but it is known to perform poorly on certain compositions — particularly those containing heavier halides.

Your task: given rA, rB, rX, nA, nB, nX for an ABX3 compound, design a one-dimensional scalar descriptor that classifies it as perovskite or non-perovskite more accurately than the Goldschmidt tolerance factor.
You may use at most 2 free parameters. Each additional free parameter incurs a 0.1-point penalty (no penalty for 2 or fewer parameters, a 0.1-point penalty for 3 parameters, and a 0.2-point penalty for 4 parameters).

## Data and Evaluation Helper

Data are in `data/TableS1.csv`. The file has 576 rows and 12 columns.
The columns are `ABX3` (compound formula), `exp_label` (`+1` perovskite, `-1` non-perovskite), `is_train` (`1` train, `-1` test), `A`, `B`, `X` (element symbols), `nA`, `nB`, `nX` (oxidation states), `rA (Ang)`, `rB (Ang)`, and `rX (Ang)` (Shannon ionic radii in angstrom).
Candidate formulas should use only `rA`, `rB`, `rX`, `nA`, `nB`, and `nX` as inputs.

Candidate code should define a descriptor with this signature:
```
def descriptor(rA, rB, rX, nA, nB, nX, params):
    ...
    return d
```
Here `params` is a one-dimensional NumPy array passed to the descriptor to be fitted by `problem.py`.

Use this evaluation flow:
```
from problem import load_train_data, train_only_evaluate

code = """
def descriptor(rA, rB, rX, nA, nB, nX, params):
    ...
    return d
"""

X_train, y_train = load_train_data()
metrics = train_only_evaluate(code, X_train, y_train)
```
The score is `metrics["val_accuracy"]`; higher is better.

## Notes

Do not modify `problem.py` or `evaluation.py`.
Do not modify `data/TableS1.csv`.
