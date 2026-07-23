# IGNOREME

## Notes to ansatz-proposer

## Notes to ansatz-reviewer

## Notes to dispatcher

After the search is complete, evaluate the best candidate using the following protocol

```
from problem import load_data, posthoc_evaluate

code = """
def descriptor(rA, rB, rX, nA, nB, nX, params):
    ...
    return d
"""

X_train, y_train, X_test, y_test, df = load_data()
metrics = posthoc_evaluate(code, X_train, y_train, X_test, y_test, df)
```
and report `metrics["test_accuracy"]` to the user.
