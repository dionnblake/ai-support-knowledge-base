# Synthetic support workflow

## Purpose
Demonstrate validated intake, queue recommendation, cited deterministic drafting and explicit local review.

## Ownership
`workflow.py` owns local event state; `demo.py` owns original synthetic inputs; `tests/` owns bounded acceptance tests.

## Local Contracts
- No network clients, live model calls, customer records or outbound actions.
- Reuse the application citation parser. Lexical sample matching is distinct from the application's Chroma/model pipeline.
- SQLite and report outputs remain under the resolved repository's `work/` directory. Tests use isolated data.
- The sample supports one worker, records local review outcomes and does not authenticate a reviewer.

## Verification
Run `python -B -m unittest discover -s examples/support_workflow/tests -v` and the root `python -B -m pytest -q`. Preserve duplicate-payload, missing-evidence, timeout, interruption and no-outbound rejection cases.

## Child DOX Index
None.
