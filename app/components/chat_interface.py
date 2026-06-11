import os
import streamlit as st
from langchain_classic.memory import ConversationBufferMemory
from app.config import UPLOAD_DIR
from app.services.qa_pipeline import query_qa_pipeline

def render_chat_input(memory: ConversationBufferMemory):
    """
    Renders the chat input bar at the bottom. When submitted, it queries the
    QA pipeline, appends results to history, and refreshes the application.
    
    Args:
        memory (ConversationBufferMemory): Conversational memory object.
    """
    # Check if there are any documents indexed
    uploaded_docs_exist = False
    if os.path.exists(UPLOAD_DIR):
        uploaded_docs_exist = len(os.listdir(UPLOAD_DIR)) > 0
        
    if not uploaded_docs_exist:
        st.info("👈 Please upload some documents in the sidebar to populate the knowledge base and start chatting!")
        return

    # Chat Input Widget
    if prompt := st.chat_input("Ask a support question about your uploaded documents..."):
        # 1. Display user message in chat container
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # 2. Append user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 3. Query QA Pipeline with spinner
        with st.chat_message("assistant"):
            with st.spinner("Searching knowledge base and formulating answer..."):
                try:
                    answer, cited_sources = query_qa_pipeline(prompt, memory)
                    st.markdown(answer)
                    
                    # Renders sources immediately for responsiveness
                    if cited_sources:
                        with st.expander("🔍 Cited Sources & Snippets", expanded=False):
                            for src in cited_sources:
                                st.markdown(
                                    f"""
                                    **[{src['index']}] {src['label']}**
                                    ```text
                                    {src['snippet']}
                                    ```
                                    """,
                                    help="Text passage retrieved from the knowledge base"
                                )
                                st.markdown("---")
                                
                    # 4. Save response to session state
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": cited_sources
                    })
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error while processing your request: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                        "sources": []
                    })
                    
        # Force a rerun to update the main view layout and history bubbles
        st.rerun()
