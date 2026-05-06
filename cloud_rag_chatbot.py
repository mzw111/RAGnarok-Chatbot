"""
Cloud Computing RAG Chatbot
FREE VERSION - Uses Groq (free LLM) + HuggingFace (free local embeddings)
No OpenAI API key or payment required!
"""

import os
os.environ['USE_TF'] = '0' # Disable TensorFlow to fix Protobuf crash

import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain_groq import ChatGroq

# Page config
st.set_page_config(
    page_title="Cloud Computing Assistant",
    page_icon="☁️",
    layout="wide"
)

# Title
st.title("☁️ Cloud Computing Notes Chatbot")
st.markdown("*Ask me anything about Cloud Computing from your notes (Units 1, 3, 4)*")
st.markdown("> 🆓 **Powered by Groq (free) + HuggingFace local embeddings (free)**")

# Sidebar for API key
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("### 🔑 Groq API Key (FREE)")
    st.markdown(
        "Get your **free** key at [console.groq.com](https://console.groq.com/keys) — "
        "no credit card required!"
    )
    api_key = st.text_input("Enter Groq API Key:", type="password", placeholder="gsk_...")
    st.markdown("---")
    st.markdown("### About")
    st.info("""
    This RAG chatbot uses:
    - **LangChain** for orchestration
    - **FAISS** for vector storage
    - **HuggingFace** for FREE local embeddings
    - **Groq + Llama 3** as FREE LLM
    - Your **Cloud Computing notes** as knowledge base
    """)

    st.markdown("### Sample Questions")
    st.markdown("""
    - What is cloud computing?
    - Explain virtualization
    - What are the cloud service models?
    - Difference between IaaS and PaaS?
    - What is load balancing?
    """)

# Initialize session state
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

@st.cache_resource(show_spinner=False)
def load_and_process_notes():
    """Load notes and create vector store using FREE local embeddings"""

    # Load the extracted text (path relative to this script)
    notes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloud_computing_notes.txt')
    with open(notes_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # Create documents
    documents = [Document(page_content=chunk) for chunk in chunks]
    return documents

@st.cache_resource(show_spinner=False)
def create_vectorstore(_documents):
    """Create FAISS vector store using FREE HuggingFace embeddings (runs locally)"""
    # all-MiniLM-L6-v2 is a fast, lightweight model — downloads once (~90MB)
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )
    vectorstore = FAISS.from_documents(_documents, embeddings)
    return vectorstore

def get_response(question, vectorstore, api_key):
    """Get response using FREE Groq LLM"""
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",   # Updated to latest free Llama 3.1 model on Groq
        temperature=0.3,
        groq_api_key=api_key
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )

    result = qa_chain({"query": question})
    return result

# Main app logic
if api_key:
    # Load documents (cached — runs once)
    with st.spinner("📚 Loading your cloud computing notes..."):
        documents = load_and_process_notes()

    # Create vectorstore if not already created
    if st.session_state.vectorstore is None:
        with st.spinner("🔍 Creating embeddings locally (first time ~30s, then cached)..."):
            st.session_state.vectorstore = create_vectorstore(documents)
        st.success(f"✅ Loaded {len(documents)} chunks from your notes! Ready to chat.")

    # Chat interface
    st.markdown("---")

    # Display chat history
    for q, a in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant"):
            st.write(a)

    # User input
    user_question = st.chat_input("Ask a question about cloud computing...")

    if user_question:
        with st.chat_message("user"):
            st.write(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = get_response(user_question, st.session_state.vectorstore, api_key)
                    answer = result['result']
                    st.write(answer)

                    # Show source chunks
                    with st.expander("📄 View source chunks used"):
                        for i, doc in enumerate(result['source_documents']):
                            st.markdown(f"**Chunk {i+1}:**")
                            st.text(doc.page_content[:300] + "...")
                    
                    # Add to chat history only on success
                    st.session_state.chat_history.append((user_question, answer))
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.info("Make sure your Groq API key is correct. Get one free at https://console.groq.com/keys")

else:
    st.warning("⚠️ Please enter your **free** Groq API key in the sidebar to start chatting!")
    st.info("""
    **How to get a FREE Groq API key (takes 2 minutes):**
    1. Go to 👉 https://console.groq.com/keys
    2. Sign up with Google/GitHub (no credit card!)
    3. Click "Create API Key"
    4. Copy and paste it in the sidebar
    
    **Why Groq?**
    - Completely FREE
    - Very fast (Llama 3 model)
    - No billing required
    """)

# Footer
st.markdown("---")
st.markdown("*Built with LangChain + Groq (Llama 3) + HuggingFace FAISS — 100% Free*")
