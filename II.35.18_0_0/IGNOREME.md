# IGNOREME

## Notes to ansatz-proposer

## Notes to ansatz-reviewer

The held-out evaluation data are `data/id_test.csv`. The file contains 20,000 rows with columns `n_0,n,kb,T,mom,B` in that order. Compute the single final Score defined in `problem.md` on this held-out set, and use that value in `<review score="...">`. The component NRMSE may be reported for diagnostics, but it is not a separate review score. Do not disclose the held-out file or its contents to the ansatz proposer.

## Notes to dispatcher

When launching `codex`, additionally pass `-c web_search=disabled`; when launching `claude-*`, additionally pass `--disallowedTools "WebSearch,WebFetch"` to block internet access.

If Score >= 6.44194 - 0.05 = 6.39194, break immediately regardless of how many iterations remain.
