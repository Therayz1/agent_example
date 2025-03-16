import streamlit as st
import asyncio
from app.agent.manus import Manus
from app.logger import logger
import time

# Sayfa yapılandırması
st.set_page_config(
    page_title="OpenManus AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        padding: 0.5rem;
        font-size: 1.1rem;
        border-radius: 0.5rem;
    }
    .stButton > button {
        width: 100%;
        padding: 0.5rem;
        font-size: 1.1rem;
        border-radius: 0.5rem;
        background-color: #FF6B6B;
        color: white;
    }
    .stButton > button:hover {
        background-color: #FF5252;
    }
    .output-container {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .status-container {
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🤖 OpenManus")
    st.markdown("---")
    st.markdown("""
    ### About
    OpenManus is an advanced AI assistant that helps you with various tasks.
    
    ### Features
    - Natural language processing
    - Task automation
    - Code generation
    - Content creation
    """)
    st.markdown("---")
    st.markdown("Made with ❤️ by OpenManus Team")

# Ana başlık
st.title("🤖 OpenManus AI Assistant")
st.markdown("Your intelligent companion for various tasks")

# Session state başlatma
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Prompt girişi
prompt = st.text_area("Enter your prompt:", height=100, placeholder="What can I help you with?")

# Progress bar ve status için kolonlar
col1, col2 = st.columns([3, 1])

async def process_prompt(prompt):
    agent = Manus()
    try:
        with st.spinner("Processing your request..."):
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # İşlem simülasyonu (gerçek işlem süresine göre ayarlanabilir)
            for i in range(100):
                time.sleep(0.1)
                progress_bar.progress(i + 1)
                status_text.text(f"Processing: {i+1}%")
            
            # Manus agent'ı çalıştır
            result = await agent.run(prompt)
            
            # Sonucu chat history'e ekle
            st.session_state.chat_history.append({
                "prompt": prompt,
                "response": result if result else "Task completed successfully!"
            })
            
            # Progress bar'ı temizle
            progress_bar.empty()
            status_text.empty()
            
            return result
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Submit butonu
if st.button("Submit", key="submit"):
    if prompt.strip():
        # Asenkron işlemi çalıştır
        result = asyncio.run(process_prompt(prompt))
        
        # Sonucu göster
        if result:
            with st.expander("Result", expanded=True):
                st.markdown(result)
    else:
        st.warning("Please enter a prompt!")

# Chat history gösterimi
if st.session_state.chat_history:
    st.markdown("### Chat History")
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        with st.expander(f"Conversation {len(st.session_state.chat_history) - i}", expanded=False):
            st.markdown("**Prompt:**")
            st.markdown(chat["prompt"])
            st.markdown("**Response:**")
            st.markdown(chat["response"])

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Version:** 1.0.0")
with col2:
    st.markdown("**Status:** Active")
with col3:
    st.markdown("**Support:** [GitHub](https://github.com)") 