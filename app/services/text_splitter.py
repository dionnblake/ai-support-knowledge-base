from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(
    documents: List[Document], 
    chunk_size: int = 1000, 
    chunk_overlap: int = 200
) -> List[Document]:
    """
    Splits a list of Documents into chunked Documents.
    
    Args:
        documents (List[Document]): The list of documents to split.
        chunk_size (int): Max size of each chunk in characters.
        chunk_overlap (int): Overlap between successive chunks in characters.
        
    Returns:
        List[Document]: List of chunked Document objects.
    """
    if not documents:
        return []
        
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True  # Keeps track of where the chunk starts in the page
    )
    
    return splitter.split_documents(documents)
