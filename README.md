# RAGnarok Chatbot 🤖☁️

A powerful, **100% Free** Retrieval-Augmented Generation (RAG) chatbot that answers questions about Cloud Computing using course notes as the knowledge base.

## 🎯 Features

- **Interactive Q&A**: Ask any questions about cloud computing concepts.
- **Smart Retrieval**: Uses FAISS vector search to find relevant content from notes.
- **Context-Aware**: Leverages **Groq** and the latest **Llama 3** for accurate, hallucinaton-free answers.
- **Completely Free**: Uses HuggingFace local embeddings and Groq's free API tier—zero cost!
- **User-Friendly**: Clean, interactive Streamlit interface.
- **Source Transparency**: Shows exactly which chunks of the notes were used to generate the answer.

## 🛠️ Tech Stack

- **LangChain**: Orchestration framework for LLM applications.
- **FAISS**: Vector database for semantic search.
- **Groq API (Llama 3.1 8B)**: Lightning-fast and free LLM for generation.
- **HuggingFace (`all-MiniLM-L6-v2`)**: Local, free embedding model for vector search.
- **Streamlit**: Web interface for an interactive frontend.

## 📦 Installation

1. **Clone/Download** this project:
   ```bash
   git clone https://github.com/mzw111/RAGnarok-Chatbot.git
   cd RAGnarok-Chatbot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Alternatively, you can run `bash setup.sh` if you are on a UNIX-like system)*

3. **Get a Groq API Key (FREE)**:
   - Go to [console.groq.com/keys](https://console.groq.com/keys).
   - Sign in and create a new API key (no credit card required!).

## 🚀 Usage

1. **Run the app**:
   ```bash
   streamlit run cloud_rag_chatbot.py
   ```

2. **Enter your Groq API key** in the left sidebar.

3. **Start asking questions!**
   - "What is cloud computing?"
   - "Explain virtualization"
   - "What are IaaS, PaaS, and SaaS?"
   - "Difference between public and private cloud?"

## 📚 How It Works

### The RAG Pipeline:

1. **Document Processing**:
   - Extracts text from the cloud computing course material (`cloud_computing_notes.txt`).
   - Splits the text into chunks (1000 characters with 200 overlap) to preserve context.

2. **Embedding & Indexing**:
   - Converts chunks into high-dimensional vectors using local HuggingFace embeddings (`all-MiniLM-L6-v2`).
   - Stores the vectors efficiently in a **FAISS** vector database.

3. **Query Processing**:
   - When a user asks a question, the query is embedded and semantically searched against the FAISS vector database.
   - The top 3 most relevant chunks are retrieved.

4. **Answer Generation**:
   - The retrieved chunks + the user's question are sent to the Groq Llama 3 LLM.
   - The LLM generates a precise answer based purely on the retrieved context.
   - The response is shown in the Streamlit UI along with the source chunks referenced!

## 🎓 Interview Talking Points

**Q: What is RAG?**
A: Retrieval-Augmented Generation. Instead of relying solely on the LLM's pre-trained knowledge, we retrieve relevant documents from our custom knowledge base first, then ask the LLM to generate answers based on that context. This drastically reduces hallucinations and adds domain-specific precision.

**Q: Why FAISS and HuggingFace?**
A: FAISS (Facebook AI Similarity Search) is highly optimized for semantic search. I combined it with local HuggingFace embeddings (`all-MiniLM-L6-v2`) to perform semantic searches locally without paying for OpenAI API embeddings.

**Q: Why Groq?**
A: Groq provides extremely fast LPU inference for open-source models like Llama 3, and it has a generous free tier. This allowed the app to run complex language tasks at no cost and with incredible speed.

**Q: What's the chunking strategy?**
A: I used 1000-character chunks with a 200-character overlap. This balances context size (enough info per chunk) with precision (not too broad). The overlap ensures concepts split across chunks aren't completely lost.

## 📝 Notes

- The first run might take ~30 seconds to download the embedding model and create the vector database locally.
- Subsequent runs are instant (vectorstore is cached).

---

**Built by**: MZW
**Domain**: Generative AI, Cloud Computing
