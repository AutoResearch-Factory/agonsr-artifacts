# ZB-vs-RS descriptor discovery

## Objective

Discover a compact explicit symbolic descriptor for predicting
$\Delta E = E_{RS} - E_{ZB}$ in binary octet compounds AB.

Positive $\Delta E$ favors zincblende; negative $\Delta E$ favors rocksalt.

## Data

Training data: `data/ZB-RS_dataset.csv`.

The dataset contains 82 binary octet compounds with DFT-LDA energy differences and 18 atomic features. The convention is that element A has smaller Mulliken electronegativity.

Reference feature descriptions: `data/ZB-RS_feature_descriptions.csv`.

| Column | Meaning |
| --- | --- |
| `Formula` | compound formula |
| `A`, `B` | element names |
| `energy_diff` | $\Delta E = E_{RS}-E_{ZB}$ in eV |
| `min_struc_type` | lower-energy structure, `RS` or `ZB` |
| `Z_A`, `Z_B` | atomic number |
| `r_s_A`, `r_s_B` | radius of maximum radial distribution of s orbital, Bohr |
| `r_p_A`, `r_p_B` | radius of maximum radial distribution of p orbital, Bohr |
| `r_d_A`, `r_d_B` | radius of maximum radial distribution of d orbital, Bohr |
| `period_A`, `period_B` | periodic-table period |
| `EA_A`, `EA_B` | electron affinity, eV |
| `IP_A`, `IP_B` | ionization potential, eV |
| `E_HOMO_A`, `E_HOMO_B` | highest occupied atomic orbital energy, eV |
| `E_LUMO_A`, `E_LUMO_B` | lowest unoccupied atomic orbital energy, eV |

## Evaluation helper

Use `evaluation.py` for loading data, computing descriptors, fitting scalar parameters, and evaluating linear-regression RMSE.

Important functions:
- `load_data()` returns `(X, y, df)`.
- `fit_params(code, df, y)` is only a reference helper for fitting `params[i]`; you may use your own method to find better parameters.
- `compute_descriptor(code, df, params)` returns the descriptor matrix.
- `evaluate_descriptor(D, y)` returns full-fit RMSE/R² and LOOCV RMSE/R².
- `save_descriptor_plot(D, y, out_path)` saves a descriptor plot.

## Candidate requirements

The candidate must propose a compact explicit 2D descriptor $(d_1,d_2)$ using the available variables.

The descriptor should be accurate under LOOCV RMSE, physically interpretable, and not tied to any particular code wrapper.

Use any analysis you need, but write all generated artifacts only to `<WORKDIR>`. Do not modify `evaluation.py`.

The final `ansatz.md` should include the descriptor formula, fitted parameters, physical intuition, full-fit metrics, LOOCV metrics, and generated artifacts.

