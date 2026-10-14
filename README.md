# AI Support Knowledge Base

**Document retrieval and a local human-reviewed support-workflow sample.**

Support teams need to connect a question with relevant documentation and keep unresolved cases visible. The existing Python/Streamlit application loads documents, retrieves passages and maps citation markers to source cards. This showcase adds a compact, isolated example of ticket intake and review.

![AI Support Knowledge Base: support overview](assets/support-overview.png)

*Locally rendered genuine output report; this is not an application UI screenshot. Read its scope and limitations below.*

**Status:** Public application source; verified local synthetic sample; original and sample offline tests passed.

[Walkthrough](docs/WALKTHROUGH.md) · [Technical explanation](docs/ARCHITECTURE.md) · [Validation scope](docs/EVIDENCE.md)

## From input to output

An original synthetic ticket reports an expired password-reset link. The sample validates it, recommends Access support, finds a matching synthetic guide and prepares a deterministic cited draft. Review remains pending. Duplicate delivery returns the same durable result; an unrelated ticket has no suggestion because its documentation is missing.

## My contribution

I brought support and escalation experience to the workflow requirements, citation presentation and human handoff. I directed AI-assisted development of the application and this bounded sample, reviewed the design and used agent-run tests. The project is independent work and does not reuse former-employer tickets or claim a paid deployment.

## Architecture and decisions

The application separates Streamlit components from document loading, chunking, embedding/vector storage and conversational QA services. Chroma stores retrieved vectors; configured model providers supply application answers. The new offline sample uses Python standard-library SQLite, lexical matching and a deterministic template, and reuses the existing citation parser. It does not replace or prove the live model/vector pipeline.

- Keep the sample integration-free: no network client or sender exists, so even an approved sample cannot contact a customer or write to a CRM.
- Persist checkpoints and event IDs: restart can recover received or retryable work, while a reused ID with a different payload is rejected. The sample is a single-worker teaching example, not a distributed queue.
- Show supporting text and require explicit review: a draft is easy to inspect; lexical overlap and citation parsing alone do not validate semantic truth.

## Validation

Nine focused unittest acceptance tests pass, covering success, duplicate delivery across restart, changed-payload rejection, missing evidence, invalid input, simulated timeout, interruption/recovery, approval boundaries and rejection. Storage recovery uses a real isolated SQLite database. The original app suite initially could not collect because dependencies were absent. After restoring its declared dependencies in an isolated local environment, the original tests and sample tests passed together: 17 tests and five unittest subtests, with three existing dependency deprecation warnings. No live model quality or CRM integration result is claimed.

## Failure and human review

Invalid tickets create no event. Missing documentation suppresses the draft. A simulated external timeout records RETRY_REQUIRED without calling an integration. Interruption is injected after a durable receipt and recovered on a new instance. Review records APPROVED_LOCAL_ONLY or REJECTED; the sample has zero outbound actions in either state.

## Limitations

The timeout and interruption are explicit simulations. This does not establish production Zendesk, Salesforce or LLM behavior. The sample does not support concurrent workers, SLAs, authenticated reviewer identity or a hosted backend. Existing citation mapping filters valid indexes but does not independently check every model claim.

## Inspect or run

Run the public offline sample with Python using the commands in docs/WALKTHROUGH.md; no paid API is required. Existing application setup remains in docs/INSTALLATION.md. Fresh installation and live application behavior require their declared dependencies and separately configured providers.
