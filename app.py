import os
import shutil
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from utils.pdf_loader import load_pdf
from utils.docx_loader import load_docx
from utils.text_loader import load_text
from utils.embedding import get_embedding_function
from utils.vector_store import get_chroma, clear_vector_store
from utils.chunking import chunk_text
from utils.query import query_vector_store

# Set a hard limit of 200MB for total uploaded file size
MAX_TOTAL_FILE_SIZE_MB = 200

# ------------------ Page Config ------------------
st.set_page_config(page_title="AI Knowledge Chatbox", layout="wide")

# ------------------ Custom Styling with Animations ------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

/* Default (Dark) Theme Styling */
.stApp {
    background-color: #0d1117;
    color: #c9d1d9;
    font-family: 'Inter', sans-serif;
    animation: fadeIn 1s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Header and title styling with Typewriter effect */
h1 {
    color: #58a6ff;
    text-shadow: 1px 1px 2px #010409;
    overflow: hidden; /* Ensures the text is not visible until animated */
    border-right: .15em solid #58a6ff; /* The animated cursor */
    white-space: nowrap;
    margin: 0 auto;
    letter-spacing: .15em;
    animation: 
      typewriter 3s steps(30, end),
      blink-caret .75s step-end infinite;
    width: 100%;
    max-width: fit-content;
}

@keyframes typewriter {
  from { width: 0 }
  to { width: 100% }
}

@keyframes blink-caret {
  from, to { border-color: transparent }
  50% { border-color: #58a6ff; }
}

h2, h3 {
    color: #58a6ff;
    text-shadow: 1px 1px 2px #010409;
}

/* Chat container for layout and scrolling */
.stChatMessage {
    display: flex;
    flex-direction: column;
    padding: 10px;
}
.chat-container {
    padding-bottom: 20px;
    height: calc(100vh - 250px);
    overflow-y: auto;
    border: 1px solid #30363d;
    border-radius: 10px;
    background-color: #161b22;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
    animation: slideInFromTop 0.8s ease-out;
}
@keyframes slideInFromTop {
    from { transform: translateY(-20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

/* Chat bubble styling with slide-in animations */
.chat-bubble-user {
    background-color: #238636;
    color: #ffffff;
    padding: 12px 16px;
    border-radius: 18px 18px 0px 18px;
    margin: 10px 0;
    align-self: flex-end;
    text-align: right;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    max-width: 80%;
    animation: slideInFromRight 0.5s ease-out;
}
@keyframes slideInFromRight {
    from { transform: translateX(20px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
.chat-bubble-bot {
    background-color: #30363d;
    color: #c9d1d9;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 0px;
    margin: 10px 0;
    align-self: flex-start;
    text-align: left;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    max-width: 80%;
    animation: slideInFromLeft 0.5s ease-out;
}
@keyframes slideInFromLeft {
    from { transform: translateX(-20px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

/* Loading animation for thinking state */
.st-spinner > div > div > div > div > div > div {
    border-color: #58a6ff;
    border-right-color: transparent;
}
.st-spinner > div > div > div > div > p {
    color: #c9d1d9;
    font-style: italic;
}
.st-spinner::before {
    content: "Thinking";
    color: #c9d1d9;
    margin-right: 5px;
    animation: loading-dots 1.5s infinite;
}
@keyframes loading-dots {
    0%, 20% { content: "Thinking"; }
    40% { content: "Thinking."; }
    60% { content: "Thinking.."; }
    80%, 100% { content: "Thinking..."; }
}

/* Interactive element styling (buttons, inputs) with animations */
.stButton button {
    border-radius: 8px;
    border: 1px solid #30363d;
    background-color: #1f2832;
    color: #c9d1d9;
    font-weight: bold;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    transition: all 0.2s ease-in-out;
}
.stButton button:hover {
    background-color: #2d3b48;
    border-color: #58a6ff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    transform: translateY(-2px);
}
.stButton button:active {
    transform: translateY(0);
}

.stTextInput > div > div > input {
    background-color: #161b22;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.6);
}

/* Sidebar styling */
.stSidebar > div:first-child {
    background-color: #0d1117;
    border-right: 1px solid #30363d;
}
.sidebar-header {
    font-size: 1.5rem;
    font-weight: 700;
    color: #58a6ff;
    margin-bottom: 20px;
}

/* Light Theme Overrides */
@media (prefers-color-scheme: light) {
    .stApp {
        background-color: #f0f2f6;
        color: #262626;
    }
    
    h1, h2, h3 {
        color: #007bff;
        text-shadow: none;
    }

    h1 {
        border-right-color: #007bff;
        animation: typewriter 3s steps(30, end), blink-caret-light .75s step-end infinite;
    }

    @keyframes blink-caret-light {
      from, to { border-color: transparent }
      50% { border-color: #007bff; }
    }

    .chat-container {
        background-color: #ffffff;
        border: 1px solid #d1d5db;
        box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.1);
    }
    
    .chat-bubble-user {
        background-color: #e0f7fa;
        color: #262626;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .chat-bubble-bot {
        background-color: #f1f5f9;
        color: #262626;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .st-spinner > div > div > div > div > div > div {
        border-color: #007bff;
        border-right-color: transparent;
    }
    .st-spinner > div > div > div > div > p {
        color: #262626;
    }
    .st-spinner::before {
        content: "Thinking";
        color: #262626;
    }

    .stButton button {
        border: 1px solid #d1d5db;
        background-color: #f7f7f7;
        color: #262626;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stButton button:hover {
        background-color: #e2e8f0;
        border-color: #007bff;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #262626;
        border: 1px solid #d1d5db;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    .stSidebar > div:first-child {
        background-color: #eef2f6;
        border-right: 1px solid #d1d5db;
    }
    .sidebar-header {
        color: #007bff;
    }
}
</style>
""", unsafe_allow_html=True)

# ------------------ State Init ------------------
if "indexed" not in st.session_state:
    st.session_state.indexed = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# New state variable to hold the query text value
if "query_text_value" not in st.session_state:
    st.session_state.query_text_value = ""
    
# State for the number of queries asked
if "query_count" not in st.session_state:
    st.session_state.query_count = 0

def clear_kb():
    # Check if the vectordb object exists before trying to clear it
    if "vectordb" in st.session_state:
        clear_vector_store(st.session_state.vectordb)
    st.session_state.indexed = False
    st.session_state.messages = []
    # Clear the query text input value
    st.session_state.query_text_value = "" 
    st.session_state.query_count = 0
    st.success("Knowledge base cleared!")

# ------------------ Sidebar ------------------
with st.sidebar:
    st.markdown("<div class='sidebar-header'>Settings</div>", unsafe_allow_html=True)
    provider = st.selectbox("Embedding provider", ["OpenAI", "Local"])
    openai_embed_model = st.text_input("OpenAI embedding model", value="text-embedding-3-small")
    collection_name = st.text_input("Collection name", value="docuchat_collection")
    st.markdown("---")

# ------------------ Main App ------------------
st.title("📚 AI Knowledge Chatbox")

uploaded_files = st.file_uploader(
    "Step 1: Upload documents", 
    type=["pdf", "docx", "txt"], 
    accept_multiple_files=True
)

if uploaded_files:
    # Check total file size
    total_size_bytes = sum(file.size for file in uploaded_files)
    total_size_mb = total_size_bytes / (1024 * 1024)
    
    if total_size_mb > MAX_TOTAL_FILE_SIZE_MB:
        st.error(f"Total file size exceeds the {MAX_TOTAL_FILE_SIZE_MB}MB limit. Please upload smaller files.")
    else:
        if st.button("Step 2: Build Knowledge Base"):
            # Clear the knowledge base before building a new one
            clear_kb()
            
            with st.spinner("Building knowledge base..."):
                docs = []
                for file in uploaded_files:
                    if file.name.endswith(".pdf"):
                        loaded_docs = load_pdf(file)
                    elif file.name.endswith(".docx"):
                        loaded_docs = load_docx(file)
                    elif file.name.endswith(".txt"):
                        loaded_docs = load_text(file)
                    else:
                        continue
                    
                    for doc in loaded_docs:
                        doc.metadata["source"] = file.name
                    
                    docs.extend(loaded_docs)

                chunks = chunk_text(docs, chunk_size=900, chunk_overlap=150)
                embed_fn = get_embedding_function(provider, openai_embed_model)
                st.session_state.embed_fn = embed_fn 
                vectordb = get_chroma(collection_name, embeddings=embed_fn)
                vectordb.add_documents(chunks)
                
                st.session_state.vectordb = vectordb
                st.session_state.indexed = True
                st.session_state.messages = []
                st.session_state.query_count = 0 # Reset query count on new KB
                st.success(f"Knowledge base built successfully from {len(uploaded_files)} files!")
                st.rerun()


# ------------------ Chat Section ------------------
if st.session_state.indexed:
    # Display chat messages from history
    with st.container(height=400, border=True):
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"<div class='chat-bubble-user'>{message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bubble-bot'>{message['content']}</div>", unsafe_allow_html=True)

    # Use a form to group the input and send button
    with st.form(key="query_form"):
        col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
        
        with col1:
            query_text = st.text_input(
                "💬 Ask your question:", 
                value=st.session_state.query_text_value,
                key="query_input",
                label_visibility="hidden"
            )
        
        with col2:
            send_button = st.form_submit_button("Send")
        
        with col3:
            # The "Satisfied / Done" button only appears after the first question is asked
            if st.session_state.query_count > 0:
                satisfied_button = st.form_submit_button("Satisfied / Done")
                if satisfied_button:
                    clear_kb()
                    st.rerun()
                    
    if send_button and query_text:
        # Increment query count
        st.session_state.query_count += 1
        
        # Get AI response
        with st.spinner("Thinking..."):
            answer = query_vector_store(
                query_text, 
                collection_name=collection_name, 
                embeddings=st.session_state.embed_fn
            )
        
        # Add user and bot messages to session state
        st.session_state.messages.append({"role": "user", "content": query_text})
        st.session_state.messages.append({"role": "bot", "content": answer})
        
        # Clear the input field after the query is processed
        st.session_state.query_text_value = ""
        st.rerun()
            
    if st.button("Clear Knowledge Base"):
        clear_kb()
        st.rerun()
else:
    st.info("Please build your knowledge base before chatting.")
