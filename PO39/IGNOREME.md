# IGNOREME

## Notes to ansatz-proposer

## Notes to ansatz-reviewer

The held-out evaluation data are `data/id_test.csv` and `data/ood_test.csv`. Each file contains 500 rows with columns `dv_dt,x,t,v` in that order. Concatenate the two files into one held-out evaluation set, compute the single final Score defined in `problem.md`, and use that value in `<review score="...">`. The component NRMSE may be reported for diagnostics, but it is not a separate review score. Do not disclose the held-out files or their contents to the ansatz proposer.

## Notes to dispatcher

When launching `codex`, additionally pass `-c web_search=disabled`; when launching `claude-*`, additionally pass `--disallowedTools "WebSearch,WebFetch"` to block internet access.

If Score >= 6.07 - 0.5 = 5.57, break immediately regardless of how many iterations remain.
