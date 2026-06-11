import streamlit as st

def render_chat_history():
    """
    Renders the chat messages currently stored in the session state.
    Each message displays its content, and assistant messages additionally
    render citations as custom expandable widgets.
    """
    # Ensure messages array exists in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        sources = msg.get("sources", [])
        
        with st.chat_message(role):
            # Render main text message
            st.markdown(content)
            
            # If assistant message contains citations, render them
            if role == "assistant" and sources:
                with st.expander("🔍 Cited Sources & Snippets", expanded=False):
                    for src in sources:
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
