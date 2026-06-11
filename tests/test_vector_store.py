import pytest
from unittest.mock import patch, MagicMock
from langchain_core.documents import Document
from app.services.vector_store import add_documents_to_store, reset_vector_store, get_vector_store

@patch("app.services.vector_store.get_embeddings")
@patch("app.services.vector_store.Chroma")
def test_get_vector_store(mock_chroma, mock_embeddings):
    mock_embeddings_inst = MagicMock()
    mock_embeddings.return_value = mock_embeddings_inst
    
    get_vector_store()
    
    mock_chroma.assert_called_once()
    assert mock_chroma.call_args[1]["collection_name"] == "support_knowledge_base"

@patch("app.services.vector_store.get_vector_store")
def test_add_documents_to_store(mock_get_store):
    mock_db = MagicMock()
    mock_get_store.return_value = mock_db
    
    docs = [Document(page_content="some content", metadata={"source": "test.txt"})]
    add_documents_to_store(docs)
    
    mock_db.add_documents.assert_called_once_with(docs)

@patch("app.services.vector_store.get_vector_store")
def test_reset_vector_store(mock_get_store):
    mock_db = MagicMock()
    mock_get_store.return_value = mock_db
    
    reset_vector_store()
    
    mock_db.delete_collection.assert_called_once()
