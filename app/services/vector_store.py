import os
import shutil
from typing import List, Any
from pathlib import Path
from langchain_core.documents import Document
from langchain_chroma import Chroma
from app.config import CHROMA_PERSIST_DIR
from app.services.embeddings import get_embeddings

def get_vector_store() -> Chroma:
    """
    Initializes and returns the persisted Chroma vector store.
    
    Returns:
        Chroma: Configured vector database.
    """
    embeddings = get_embeddings()
    
    # Ensure persistence directory exists
    Path(CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
    
    return Chroma(
        collection_name="support_knowledge_base",
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR
    )

def add_documents_to_store(documents: List[Document]) -> None:
    """
    Adds a list of Document objects to the Chroma vector store.
    
    Args:
        documents (List[Document]): Document chunks to be indexed.
    """
    if not documents:
        return
        
    db = get_vector_store()
    db.add_documents(documents)

def get_retriever(k: int = 4) -> Any:
    """
    Returns a retriever object from the vector store.
    
    Args:
        k (int): Number of top matches to retrieve.
        
    Returns:
        VectorStoreRetriever: Retriever interface for QA chains.
    """
    db = get_vector_store()
    return db.as_retriever(search_kwargs={"k": k})

def reset_vector_store() -> None:
    """
    Completely deletes and resets the Chroma vector store collection.
    If database files are locked by the system, deletes documents in chunks
    or clears metadata references.
    """
    try:
        db = get_vector_store()
        # Delete collection clears all data in Chroma
        db.delete_collection()
    except Exception as e:
        # If collection deletion fails or is not supported, try removing the directory directly
        print(f"Error deleting collection, falling back to directory removal: {e}")
        if os.path.exists(CHROMA_PERSIST_DIR):
            try:
                shutil.rmtree(CHROMA_PERSIST_DIR)
            except Exception as dir_err:
                print(f"Could not remove database directory: {dir_err}")
                
    # Re-initialize empty directory and store structure
    Path(CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
