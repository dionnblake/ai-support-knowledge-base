from typing import Any
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_openai import OpenAIEmbeddings
from app.config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL, EMBEDDING_PROVIDER

def get_embeddings() -> Any:
    """
    Initializes and returns the selected embedding model (OpenAI or Local FastEmbed).
    
    Returns:
        Any: Configured embedding model.
        
    Raises:
        ValueError: If OpenAI is selected and the API key is missing.
    """
    if EMBEDDING_PROVIDER == "local":
        return FastEmbedEmbeddings()
        
    if not OPENAI_API_KEY:
        raise ValueError(
            "OpenAI API Key is missing. Please make sure to add it to your "
            "environment variables or a `.env` file as OPENAI_API_KEY."
        )
        
    return OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY,
        model=OPENAI_EMBEDDING_MODEL
    )
