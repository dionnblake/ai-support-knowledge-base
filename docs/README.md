# AI Support Agent Knowledge Base - In-depth Guide

This document provides a detailed overview of the design, architecture, setup instructions, and workflows for the AI Support Agent Knowledge Base.

---

## Architecture Diagram

Here is the flow of information through the system during document ingestion and questioning:

```
[Document Ingestion]
  Upload files (PDF, DOCX, TXT) via Sidebar
      ├──> app/services/document_loader.py (extracts text)
      ├──> app/services/text_splitter.py (chunks text into overlapping segments)
      └──> app/services/embeddings.py (calls OpenAI embeddings api)
            └──> app/services/vector_store.py (saves vectors & metadata in ChromaDB)

[Chat / Query Execution]
  User enters query in Main Canvas
      ├──> app/services/qa_pipeline.py (initializes LLM, memory, & retriever)
            ├──> Retrieval: Queries ChromaDB for similar chunks
            ├──> Prompting: Assembles history, context, and query
            └──> LLM (gpt-4o-mini): Formulates answer citing indexes e.g., [1]
      └──> app/utils/citation_utils.py (resolves bracketed numbers to source metadata & text snippets)
            └──> Streamlit UI renders conversation and expandable Sources section
```

---

## Tech Stack & Design Choices

1. **Streamlit (Front End)**: Creates a fast, responsive UI with stateful conversation memory. Styled with a custom modern dark-theme CSS layout (Outfit font, gradient header, card styling).
2. **LangChain (LLM Orchestration)**: Handles the RetrievalQA and conversational history components, facilitating memory management across follow-up questions.
3. **OpenAI API**:
   - Embeddings: `text-embedding-3-small` (1536-dimensional, highly cost-effective).
   - Chat: `gpt-4o-mini` (highly performant and fast support reasoning).
4. **ChromaDB (Vector Database)**: Lightweight, runs entirely locally, and persists data under `./data/chromadb/`.
5. **Document Ingestion**:
   - `pypdf` for extracting PDF pages with metadata.
   - `python-docx` for parsing Microsoft Word documents.
   - Standard text loaders for `.txt` files.

---

## Installation & Running

### 1. Prerequisites
- Python 3.9+
- OpenAI API Key

### 2. Setup Virtual Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your-openai-api-key-here
```

### 5. Run Application
```bash
streamlit run app/main.py
```

---

## Verification & Testing

To run the unit tests offline:
```bash
pytest tests/
```

### Mocked Testing Strategy
The unit tests in `tests/` leverage `unittest.mock` to mock out all embedding and chat calls to OpenAI. This ensures the tests are fully executable offline and do not consume OpenAI API tokens.

---

## Current Limitations & Future Improvements
- **Document Formats**: Current parsers handle standard layout PDFs and text. Complex PDFs containing multi-column tables, scanned image pages (requiring OCR), or heavy formatting may see reduced retrieval accuracy.
- **Scale**: ChromaDB is running in local persistent mode. For enterprise deployment with millions of documents, migrating to a hosted cloud vector database (e.g. Pinecone, pgvector) would be recommended.
- **Concurrent Sessions**: The current architecture is designed for single-user testing/demonstration, utilizing memory within the local streamlit session context.
