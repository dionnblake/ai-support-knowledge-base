# AI Support Knowledge Base: walkthrough

An original synthetic ticket reports an expired password-reset link. The sample validates it, recommends Access support, finds a matching synthetic guide and prepares a deterministic cited draft. Review remains pending. Duplicate delivery returns the same durable result; an unrelated ticket has no suggestion because its documentation is missing.

1. Open the overview and read the mode/status caption.
2. Compare the input with the displayed workflow or returned result.
3. Open the evidence image and inspect provenance, failure or review state.
4. Explain the limitation before discussing the design tradeoff.

This is an approximately 60–90 second interview walkthrough. No recorded video was produced.

Run the public offline sample with Python using the commands in docs/WALKTHROUGH.md; no paid API is required. Existing application setup remains in docs/INSTALLATION.md. Fresh installation and live application behavior require their declared dependencies and separately configured providers.

From the repository root:

```powershell
python -B -m examples.support_workflow.demo
python -B -m unittest discover -s examples/support_workflow/tests -v
```

The demonstration writes only to the repository’s work/support-workflow-demo directory. It never opens data/chromadb or app configuration. Review is pending by default; Workflow.review records a local outcome and never sends anything.
