# IGNOREME

## Notes to ansatz-proposer

- Do not use `data/Vali.csv` for regression. Fit only on `data/Train_2025409.csv`.
- Always make a final parity plot.

## Notes to ansatz-reviewer

- The validation set is `data/Vali.csv`. Check whether the ansatz proposer used any information from `Vali.csv` during fitting. If so, refit on the training data and score the refitted model to prevent inflated validation performance. The `Diameter` and `GroupID` columns in `Vali.csv` are unused.
- Update the parity plot so it includes both training data and validation data in different colors.
