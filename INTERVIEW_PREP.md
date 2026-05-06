# Interview Preparation Guide - Cloud Computing RAG Chatbot

## 🎯 Project Elevator Pitch (30 seconds)

"I built a RAG-based chatbot that answers questions about Cloud Computing using my course notes. It uses LangChain to orchestrate the pipeline - I extract text from PDFs, chunk them, create vector embeddings with OpenAI, store them in FAISS for semantic search, and then use GPT-3.5 to generate answers based on retrieved context. Built with Streamlit for the UI."

## 🔥 Key Interview Questions & Answers

### 1. **What is RAG and why did you use it?**

**Answer**: 
"RAG stands for Retrieval-Augmented Generation. Instead of just asking an LLM a question and hoping it knows the answer from training, RAG first retrieves relevant documents from a knowledge base, then uses those as context for the LLM to generate an answer.

I used it because:
- Reduces hallucinations - the LLM bases answers on actual documents
- Adds domain-specific knowledge not in the LLM's training
- More cost-effective than fine-tuning
- Provides source transparency - users can see where answers come from"

### 2. **Walk me through your RAG pipeline**

**Answer**:
"Sure! Here's the flow:

**Indexing Phase (done once):**
1. Extract text from PDFs using PyMuPDF
2. Split text into 1000-character chunks with 200-char overlap
3. Convert each chunk to a 1536-dimensional vector using OpenAI's text-embedding-ada-002
4. Store vectors in FAISS index for fast similarity search

**Query Phase (each question):**
1. User asks a question
2. Convert question to vector using same embedding model
3. FAISS finds top 3 most similar document chunks
4. Send question + retrieved chunks to GPT-3.5-turbo
5. LLM generates answer based on that context
6. Return answer with source references"

### 3. **Why did you choose these specific technologies?**

**Answer**:
- **LangChain**: Industry-standard framework, makes it easy to chain components
- **FAISS**: Facebook's vector DB - fast, efficient, works offline, free
- **OpenAI**: High-quality embeddings and LLM, easy to use API
- **Streamlit**: Quick to build interactive UIs, perfect for demos
- **Alternatives I considered**: Pinecone (but costs money), Llama (slower), Chroma (less mature)"

### 4. **What's your chunking strategy and why?**

**Answer**:
"I use 1000 characters per chunk with 200-character overlap.

**Why 1000?** 
- Big enough to contain complete concepts
- Small enough to be precise when retrieving
- Fits well within token limits when sending to LLM

**Why 200 overlap?**
- Prevents concepts split across chunk boundaries from being lost
- Ensures continuity between chunks

I tested different sizes - 500 was too fragmented, 2000 retrieved too much irrelevant content."

### 5. **How do you handle the cost of API calls?**

**Answer**:
"Several strategies:
- Used GPT-3.5-turbo instead of GPT-4 (10x cheaper)
- Cache the vector embeddings - only create once
- Limited retrieval to top 3 chunks (instead of 5-10)
- Set temperature to 0.3 for concise answers
- With free tier $5 credit, this runs hundreds of queries for free"

### 6. **What are the limitations of your system?**

**Answer** (being honest shows maturity):
"A few limitations:
- No conversation memory - each question is independent
- Only works with my cloud computing notes - not general knowledge
- Chunk boundaries might split important context
- Depends on OpenAI API (not fully offline)
- No evaluation metrics to measure answer quality

**What I'd improve:**
- Add conversation history using LangChain memory
- Implement hybrid search (semantic + keyword)
- Add re-ranking for better chunk selection
- Build evaluation with RAGAS framework
- Support more file formats beyond PDF"

### 7. **How do you evaluate if your RAG system is working well?**

**Answer**:
"Right now it's manual testing, but proper evaluation would use:
- **Retrieval Metrics**: Check if relevant chunks are retrieved (precision/recall)
- **Generation Metrics**: BLEU/ROUGE scores against ground truth
- **End-to-End**: Frameworks like RAGAS measure faithfulness, relevance, context precision
- **User Feedback**: Thumbs up/down on answers

For this project I manually tested with ~10 questions from different units and checked if answers matched my notes."

### 8. **Can you explain vector embeddings simply?**

**Answer**:
"Sure! Think of embeddings as converting text into coordinates in high-dimensional space. Similar concepts end up close together.

For example:
- 'What is cloud computing?' → [0.2, 0.8, 0.1, ...]
- 'Define cloud computing' → [0.21, 0.79, 0.11, ...] (very close!)
- 'How to bake cookies?' → [0.9, 0.1, 0.7, ...] (far away)

The 1536 numbers capture semantic meaning. When I search, I find chunks whose vectors are closest to the question vector."

### 9. **What's the difference between your RAG approach and fine-tuning?**

**Answer**:
"**RAG:**
- Adds external knowledge at query time
- Can update knowledge by changing documents
- Cheaper and faster to implement
- LLM doesn't 'learn' the data

**Fine-tuning:**
- Permanently updates the model weights
- Model 'memorizes' the training data
- Expensive (requires GPU, time, data)
- Better for changing behavior/style, not adding facts

For my use case (domain knowledge that might update), RAG was better."

### 10. **How would you deploy this to production?**

**Answer**:
"For production I'd:
1. **Hosting**: Deploy on Streamlit Cloud or AWS EC2
2. **Security**: Environment variables for API keys, rate limiting
3. **Database**: Move from FAISS to Pinecone/Weaviate for persistence
4. **Caching**: Redis cache for common questions
5. **Monitoring**: Log queries, track costs, measure latency
6. **Scale**: Load balancer, async processing for multiple users
7. **CI/CD**: GitHub Actions for automated testing and deployment"

## 🎨 Technical Deep-Dives (If Interviewer Probes)

### Vector Search Math
"FAISS uses cosine similarity: measures angle between vectors. Score of 1 = identical, 0 = orthogonal, -1 = opposite. I retrieve chunks with highest cosine similarity to the query."

### Why Overlap Matters
"Without overlap, if concept X is explained across 2 chunks, we might retrieve chunk 1 (incomplete explanation) and miss chunk 2. With overlap, chunk 1 includes start of chunk 2's content, so we get continuity."

### Token Optimization
"Each API call has token limits. I count: question tokens + retrieved chunks tokens + answer tokens < 4096 (GPT-3.5 limit). That's why I limit to 3 chunks of 1000 chars each."

## 📊 Project Stats to Mention

- 540K characters extracted from 3 PDFs
- ~540 document chunks created
- 1536-dimensional embeddings (OpenAI ada-002)
- Retrieves top-3 chunks per query
- Response time: ~2-3 seconds per question
- Cost: ~$0.01 per session

## 🚀 Good Talking Points

✅ "I iterated on chunk size - started with 500, found answers too fragmented"
✅ "I added source document view so users can verify answers"
✅ "I cached the vectorstore to avoid re-embedding on every run"
✅ "I used RecursiveCharacterTextSplitter to respect sentence boundaries"
✅ "Temperature of 0.3 balances accuracy with natural language"

## ❌ Things NOT to Say

❌ "I just copied code from the internet" (even if you started with a template)
❌ "I don't really understand embeddings" (read up on them!)
❌ "It always gives perfect answers" (be honest about limitations)
❌ "I haven't actually tested it much" (test it!)

## 🎓 Concepts to Brush Up On

Before interview, review:
- What are transformers/attention mechanisms (basics)
- Difference between embeddings and LLMs
- Vector similarity metrics (cosine, euclidean, dot product)
- Token counting and context windows
- Basic prompt engineering
- Semantic search vs keyword search

## 💪 Confidence Builders

You can HONESTLY say:
- "I built this from scratch using LangChain"
- "I processed my actual course notes into a working system"
- "I understand the RAG pipeline end-to-end"
- "I can explain each component and why I chose it"
- "I've tested it with real questions and iterated on the design"

---

**Pro Tip**: Run the app 5-10 times, ask different questions, see what works and what doesn't. This hands-on experience will make you confident in interviews!
