# AI Support Agent Knowledge Base

A modern, responsive Retrieval-Augmented Generation (RAG) customer support application built using **Streamlit**, **LangChain**, **ChromaDB**, and **OpenAI**. 

This repository allows customer support agents to upload document archives (manuals, guides, FAQs), parse/index them into a local vector database, and chat with an intelligent agent who answers questions with **verifiable inline source citations**.

---

## Key Features

- **Multi-Format Document Upload**: Ingest and process PDF, DOCX, and TXT files instantly.
- **Conversational Memory**: Follow-up questions are parsed in context to maintain full support thread history.
- **Inline Citations**: Every claim is cited inline (e.g. `[1]`, `[2]`), mapping to an expandable source card containing the document filename, page number, and the exact text snippet retrieved.
- **Local Persistence & Reset**: Vectors are persisted in a local database directory (`./data/chromadb`). The entire database can be wiped clean via a single click in the UI.
- **Offline Test Suite**: Pytest tests are mock-configured to execute offline and token-free.

---

## Directory Structure

```text
ai-support-knowledge-base/
│
├── app/                             # Main application code
│   ├── config.py                    # Environment validation & constants
│   ├── main.py                      # Streamlit app orchestration & Custom CSS
│   ├── components/                  # Reusable UI elements
│   │   ├── file_upload.py           # Ingestion panel & document manager
│   │   ├── chat_interface.py        # Input handling & QA flow execution
│   │   └── history_display.py       # Bubble thread & citation drawer renderer
│   ├── services/                    # Backend services
│   │   ├── document_loader.py       # PDF, DOCX, and TXT parsers
│   │   ├── text_splitter.py         # Recursive text partitioner
│   │   ├── embeddings.py            # OpenAI embedding connector
│   │   ├── vector_store.py          # Chroma collection operations
│   │   └── qa_pipeline.py           # Conversational Retrieval QA chain
│   └── utils/                       # Utility helpers
│       ├── file_utils.py            # Upload disk persistence helpers
│       └── citation_utils.py        # Citation tag & mapping parser
│
├── data/                            # Persistent data storage
│   └── sample_docs/                 # Test documents (user_manual, faq)
│
├── tests/                           # Pytest offline test suite
│   ├── test_document_loader.py      # Loader unit tests
│   ├── test_vector_store.py         # Database integration tests
│   └── test_qa_pipeline.py          # QA pipeline unit tests
│
├── docs/                            # In-depth guides & assets
│   └── README.md                    # Detailed system documentation
│
├── .gitignore                       # Git exclusion pattern rules
└── requirements.txt                 # Project dependencies list
```

---

## Quick Start

1. **Clone & Setup Environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate # Windows
   pip install -r requirements.txt
   ```

2. **Configure API Keys**:
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```

3. **Launch the App**:
   ```bash
   streamlit run app/main.py
   ```

4. **Verify Offline Tests**:
   ```bash
   pytest tests/
   ```
