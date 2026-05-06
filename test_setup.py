"""
Quick test script to verify the RAG setup works
Run this before the full Streamlit app
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os

print("[TEST] Testing RAG Components...\n")

# Test 1: Load notes
print("1. Loading cloud computing notes...")
try:
    notes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloud_computing_notes.txt')
    with open(notes_path, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"   [OK] Loaded {len(text)} characters")
except Exception as e:
    print(f"   [FAIL] Error: {e}")
    exit(1)

# Test 2: Create chunks
print("\n2. Creating text chunks...")
try:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(text)
    print(f"   [OK] Created {len(chunks)} chunks")
    print(f"   Sample chunk: {chunks[0][:100]}...")
except Exception as e:
    print(f"   [FAIL] Error: {e}")
    exit(1)

# Test 3: Check imports
print("\n3. Checking dependencies...")
try:
    import streamlit
    import langchain
    import faiss
    import openai
    print("   [OK] All dependencies installed")
except ImportError as e:
    print(f"   [FAIL] Missing dependency: {e}")
    exit(1)

print("\n[OK] All checks passed! Ready to run the chatbot.")
print("\nNext steps:")
print("   1. Run: streamlit run cloud_rag_chatbot.py")
print("   2. Enter your API key in the sidebar")
print("   3. Start asking questions!")
