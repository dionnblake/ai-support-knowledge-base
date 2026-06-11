import re
from pathlib import Path
from typing import List, Dict, Any, Tuple

def get_source_name(file_path: str) -> str:
    """
    Extracts the base filename from a full path.
    
    Args:
        file_path (str): The full path to the source file.
        
    Returns:
        str: The filename (e.g., 'user_manual.pdf').
    """
    if not file_path:
        return "Unknown Source"
    return Path(file_path).name

def format_source_label(file_path: str, page: Any = None) -> str:
    """
    Formats a user-friendly label for a source (e.g. 'manual.pdf (Page 3)').
    
    Args:
        file_path (str): Path to the source file.
        page (Any): Page number (integer, string, or None).
        
    Returns:
        str: Formatted label.
    """
    filename = get_source_name(file_path)
    if page is not None:
        # Check if page is 0-indexed and make it 1-indexed for display,
        # or if it's already 1-indexed. We assume standard langchain loaders
        # return 0-indexed or 1-indexed pages. Let's make it user friendly.
        try:
            page_num = int(page)
            # Standard pypdf loader pages are 0-indexed, so add 1 for user display
            return f"{filename} (Page {page_num + 1})"
        except (ValueError, TypeError):
            return f"{filename} (Page {page})"
    return filename

def parse_citations(answer: str, source_documents: List[Any]) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Parses the answer for citation markers like [1], [2] and maps them to the actual
    retrieved documents. Ensures we only list sources that were actually cited in the text.
    
    Args:
        answer (str): The text output from the LLM.
        source_documents (List[Document]): The list of LangChain Document objects retrieved.
        
    Returns:
        Tuple[str, List[Dict[str, Any]]]: 
            - The text answer (cleaned/standardized if necessary).
            - A list of dictionary objects containing cited source details:
              { 'index': int, 'source_name': str, 'page': int/None, 'label': str, 'snippet': str }
    """
    # Find all citation matches of format [1], [2], etc.
    matches = re.findall(r'\[(\d+)\]', answer)
    
    cited_indices = set()
    for m in matches:
        try:
            idx = int(m)
            # 1-indexed from the LLM prompt instruction
            if 1 <= idx <= len(source_documents):
                cited_indices.add(idx)
        except ValueError:
            continue
            
    cited_sources = []
    # Re-map/sort cited documents for the display drawer
    for idx in sorted(cited_indices):
        doc = source_documents[idx - 1]
        metadata = doc.metadata
        
        file_path = metadata.get("source", "Unknown")
        page = metadata.get("page", None)
        
        cited_sources.append({
            "index": idx,
            "source_name": get_source_name(file_path),
            "page": page,
            "label": format_source_label(file_path, page),
            "snippet": doc.page_content.strip()
        })
        
    return answer, cited_sources
