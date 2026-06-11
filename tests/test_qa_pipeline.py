import pytest
from unittest.mock import patch, MagicMock
from langchain_core.documents import Document
from langchain_classic.memory import ConversationBufferMemory
from app.services.qa_pipeline import query_qa_pipeline

@patch("app.services.qa_pipeline.get_qa_pipeline")
def test_query_qa_pipeline(mock_get_pipeline):
    # Setup mocks
    mock_chain = MagicMock()
    mock_get_pipeline.return_value = mock_chain
    
    # Setup mock return value for invoke
    mock_doc = Document(
        page_content="This is the text snippet from page 1.",
        metadata={"source": "user_guide.pdf", "page": 0}
    )
    mock_chain.invoke.return_value = {
        "answer": "This is the answer [1] referencing source.",
        "source_documents": [mock_doc]
    }
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        return_messages=True
    )
    
    # Run query
    ans, sources = query_qa_pipeline("How to do something?", memory)
    
    # Verify Conversational chain is invoked
    mock_chain.invoke.assert_called_once_with({"question": "How to do something?"})
    
    # Verify outputs and citations parsing
    assert "This is the answer [1]" in ans
    assert len(sources) == 1
    assert sources[0]["index"] == 1
    assert sources[0]["source_name"] == "user_guide.pdf"
    assert sources[0]["page"] == 0
    assert sources[0]["label"] == "user_guide.pdf (Page 1)"
    assert sources[0]["snippet"] == "This is the text snippet from page 1."
