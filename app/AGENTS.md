# APP CONTRACT (DOX)

This document governs the Streamlit application logic, backend services, and utilities.

## Scope & Ownership
- **Owner**: Data Engineer, AI Engineer, Front-End Developer
- **Scope**: All files under `app/`, including configurations, UI components, backend integrations, and formatting helpers.

## Rules & Standards
1. **Modularity**: Services (e.g., loaders, splitters, vector stores, QA pipelines) must be isolated from Streamlit UI code. UI files in `app/components/` must only manage rendering and use the state/services via clean interfaces.
2. **Type Hints & Docstrings**: Every function must have Python type hints and a clear docstring explaining parameters, return type, and purpose.
3. **No Local Hardcoding**: All secrets and models must be resolved through `app/config.py`. Never read `os.environ` directly in services or components.
4. **Error Handling**: Use try-except blocks in services to handle file parser issues, missing API keys, or empty vector store queries gracefully. Propagate errors as descriptive exceptions or return objects.

## Child DOX Index
None. All subfolders under `app/` are governed directly by this document.
