# TESTS CONTRACT (DOX)

This document governs unit tests in the `tests/` directory.

## Scope & Ownership
- **Owner**: DevOps / Tester
- **Scope**: All testing configurations and scripts located within `tests/`.

## Rules & Standards
1. **Offline-first / Mocking**: All tests interacting with external APIs (specifically OpenAI API requests for Embeddings and Chat) must use `unittest.mock` or `pytest-mock`. Under no circumstances should test runs fail because an API key is missing or the environment is offline.
2. **Local Vector Store testing**: Tests for vector storage may use standard mocked embeddings, but should verify correct schema, key-value mappings, and retrieval flows.
3. **Naming Convention**: Test files must start with `test_` and test functions must start with `test_`.
4. **Clean runs**: Running `pytest tests/` from the root workspace must succeed with zero failures.

## Child DOX Index
None.
