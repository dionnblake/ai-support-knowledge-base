import streamlit as st
from pathlib import Path
from app.config import UPLOAD_DIR
from app.utils.file_utils import save_uploaded_file, clear_directory
from app.utils.citation_utils import get_source_name
from app.services.document_loader import load_document
from app.services.text_splitter import split_documents
from app.services.vector_store import add_documents_to_store, reset_vector_store

def render_file_upload_sidebar():
    """
    Renders the sidebar containing the document upload interface,
    list of indexed documents, and the reset button.
    """
    st.sidebar.markdown("### 📂 Document Ingestion")
    
    uploaded_files = st.sidebar.file_uploader(
        "Upload reference documents (PDF, DOCX, TXT)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="Upload user manuals, FAQs, or support articles to add to the knowledge base."
    )
    
    # Process uploads
    if uploaded_files:
        new_files_processed = False
        with st.sidebar.status("Processing documents...", expanded=True) as status:
            for uploaded_file in uploaded_files:
                # To prevent double-processing in Streamlit reruns,
                # check if the file is already processed or exists in UPLOAD_DIR
                target_path = Path(UPLOAD_DIR) / uploaded_file.name
                if not target_path.exists():
                    st.write(f"Parsing `{uploaded_file.name}`...")
                    try:
                        # 1. Save file locally
                        local_path = save_uploaded_file(uploaded_file)
                        
                        # 2. Parse document
                        raw_docs = load_document(local_path)
                        st.write(f"Loaded {len(raw_docs)} pages/sections.")
                        
                        # 3. Split document
                        chunks = split_documents(raw_docs)
                        st.write(f"Split into {len(chunks)} passages.")
                        
                        # 4. Generate embeddings and store in Chroma
                        st.write("Indexing vectors in database...")
                        add_documents_to_store(chunks)
                        
                        new_files_processed = True
                        st.write(f"✅ `{uploaded_file.name}` indexed successfully!")
                    except Exception as e:
                        st.error(f"❌ Error indexing `{uploaded_file.name}`: {e}")
            
            status.update(label="Ingestion complete!", state="complete", expanded=False)
            
        if new_files_processed:
            st.success("Knowledge base updated!")
            st.rerun()

    # List of current documents
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📄 Indexed Documents")
    
    upload_path = Path(UPLOAD_DIR)
    current_docs = list(upload_path.glob("*")) if upload_path.exists() else []
    
    if current_docs:
        for idx, doc_path in enumerate(current_docs, 1):
            st.sidebar.caption(f"{idx}. 📁 {get_source_name(str(doc_path))}")
            
        # Reset Database Button
        st.sidebar.markdown("---")
        if st.sidebar.button("🗑️ Reset Database", use_container_width=True, type="secondary", help="Clear all documents from memory and disk."):
            with st.spinner("Clearing database and files..."):
                # Clear ChromaDB
                reset_vector_store()
                # Clear uploads folder
                clear_directory(UPLOAD_DIR)
                # Clear chat history in session state
                if "messages" in st.session_state:
                    st.session_state.messages = []
                if "chat_history" in st.session_state:
                    st.session_state.chat_history.clear()
            st.sidebar.success("Database reset complete!")
            st.rerun()
    else:
        st.sidebar.info("No documents uploaded yet. Upload files to get started!")
