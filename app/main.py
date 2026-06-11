import streamlit as st
from langchain_classic.memory import ConversationBufferMemory

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="AI Support Agent - Knowledge Base",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import components after page config
from app.components.file_upload import render_file_upload_sidebar
from app.components.history_display import render_chat_history
from app.components.chat_interface import render_chat_input

# Inject Custom Sleek Modern CSS for Rich Aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    /* Global Font Override */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main Layout Vibe */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(9, 12, 22) 90%);
        color: #f1f5f9;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Header Card (Glassmorphic) */
    .header-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818cf8 10%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .header-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 300;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.1);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        color: #c084fc !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Conversation Buffer Memory in Session State
if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        return_messages=True
    )

def main():
    # Render Sleek Header Card
    st.markdown("""
    <div class="header-card">
        <div class="header-title">🤖 AI Customer Support Knowledge Base</div>
        <div class="header-subtitle">Upload service documents, user manuals, or FAQs to chat, search, and troubleshoot with verified inline citations.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render Document Ingestion Panel in Sidebar
    render_file_upload_sidebar()
    
    # Main Chat Workspace Area
    chat_container = st.container()
    
    # Render Conversation History
    with chat_container:
        render_chat_history()
        
    # Render User Chat Input Box
    render_chat_input(st.session_state.chat_memory)

if __name__ == "__main__":
    main()
