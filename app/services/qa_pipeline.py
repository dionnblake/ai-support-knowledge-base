from typing import Dict, Any, Tuple, List
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.config import (
    OPENAI_API_KEY,
    OPENAI_LLM_MODEL,
    API_PROVIDER,
    OPENROUTER_API_KEY,
    OPENROUTER_LLM_MODEL
)
from app.services.vector_store import get_retriever
from app.utils.citation_utils import parse_citations

# Custom Prompt for QA combine docs
QA_TEMPLATE = """You are a professional AI Customer Support Agent. Answer the user's question using ONLY the provided context documents. 

Guidelines:
1. If the context does not contain the answer, politely state that you do not have that information in your knowledge base. Do not make up answers.
2. Cite the source documents inline using brackets, e.g., [1], [2], etc.
3. The context documents are listed below sequentially. The first "Source Document" is [1], the second is [2], the third is [3], and so on.
4. Always attribute information to its corresponding citation.

Context Documents:
{context}

Chat History:
{chat_history}

Question: {question}

Helpful Answer:"""

# Standalone question generator prompt
CONDENSE_QUESTION_TEMPLATE = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

def get_qa_pipeline(memory: ConversationBufferMemory) -> ConversationalRetrievalChain:
    """
    Assembles and returns a ConversationalRetrievalChain instance.
    
    Args:
        memory (ConversationBufferMemory): The Streamlit session memory to persist history.
        
    Returns:
        ConversationalRetrievalChain: The configured QA chain.
    """
    if API_PROVIDER == "openrouter":
        if not OPENROUTER_API_KEY:
            raise ValueError("OpenRouter API Key is missing. Check your .env file.")
        llm = ChatOpenAI(
            model=OPENROUTER_LLM_MODEL,
            temperature=0.0,
            openai_api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )
    else:
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API Key is missing. Check your .env file.")
        llm = ChatOpenAI(
            model=OPENAI_LLM_MODEL,
            temperature=0.0,
            openai_api_key=OPENAI_API_KEY
        )
    
    retriever = get_retriever()
    
    qa_prompt = PromptTemplate(
        template=QA_TEMPLATE,
        input_variables=["context", "chat_history", "question"]
    )
    
    condense_prompt = PromptTemplate(
        template=CONDENSE_QUESTION_TEMPLATE,
        input_variables=["chat_history", "question"]
    )
    
    # Format how documents are concatenated into the prompt
    document_prompt = PromptTemplate(
        input_variables=["page_content", "source", "page"],
        template="Source Document:\nSource file: {source}\nPage reference: {page}\nContent: {page_content}"
    )
    
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        condense_question_prompt=condense_prompt,
        combine_docs_chain_kwargs={
            "prompt": qa_prompt,
            "document_prompt": document_prompt
        }
    )
    
    return qa_chain

def query_qa_pipeline(
    query: str, 
    memory: ConversationBufferMemory
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Queries the QA pipeline, parses citation indices, and returns the response and cited sources.
    
    Args:
        query (str): User query string.
        memory (ConversationBufferMemory): Conversational memory object.
        
    Returns:
        Tuple[str, List[Dict[str, Any]]]:
            - The textual answer from the LLM.
            - A list of cited sources mapped with metadata and snippets.
    """
    qa_chain = get_qa_pipeline(memory)
    
    # Run the query
    result = qa_chain.invoke({"question": query})
    
    answer = result.get("answer", "")
    source_documents = result.get("source_documents", [])
    
    # Parse citations and map source documents
    parsed_answer, cited_sources = parse_citations(answer, source_documents)
    
    return parsed_answer, cited_sources
