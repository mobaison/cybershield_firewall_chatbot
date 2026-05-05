#!/bin/bash

# Define the root project name
PROJECT_NAME="hospital_chatbot"

echo "Creating project structure for: $PROJECT_NAME..."

# Create Directories
mkdir -p $PROJECT_NAME/rag
mkdir -p $PROJECT_NAME/data
mkdir -p $PROJECT_NAME/templates

# Create Root Files
touch $PROJECT_NAME/app.py
touch $PROJECT_NAME/requirements.txt

# Create .env.example with placeholders
cat <<EOT >> $PROJECT_NAME/.env.example
PINECONE_API_KEY=your_pinecone_key_here
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_gemini_key_here
FLASK_ENV=development
EOT

# Create RAG module files
touch $PROJECT_NAME/rag/pipeline.py
touch $PROJECT_NAME/rag/embedder.py
touch $PROJECT_NAME/rag/vector_store.py
touch $PROJECT_NAME/rag/gemini_client.py
touch $PROJECT_NAME/rag/history.py

# Create Data and UI files
touch $PROJECT_NAME/data/hospital_data.py
touch $PROJECT_NAME/templates/index.html

# Summary
echo "-----------------------------------------------"
echo "Success! Directory structure created."
echo "Next steps:"
echo "1. cd $PROJECT_NAME"
echo "2. cp .env.example .env (and add your keys)"
echo "3. python3 -m venv venv && source venv/bin/activate"
echo "-----------------------------------------------"