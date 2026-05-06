#!/bin/bash

echo "========================================="
echo "Cloud Computing RAG Chatbot - Quick Setup"
echo "========================================="
echo ""

# Check Python
echo "✓ Checking Python installation..."
python3 --version

echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the chatbot:"
echo "   streamlit run cloud_rag_chatbot.py"
echo ""
echo "⚠️  You'll need an OpenAI API key:"
echo "   Get it from: https://platform.openai.com/api-keys"
echo ""
