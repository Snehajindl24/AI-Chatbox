📚 DocuChat AI: Chat with your Documents
DocuChat AI is a powerful and intuitive chatbot that allows you to have intelligent conversations with your own documents. By leveraging Retrieval-Augmented Generation (RAG), this app builds a knowledge base from your uploaded files and provides accurate, context-aware answers to your questions.

Whether you're a student studying for an exam, a professional needing quick access to company policies, or a researcher organizing information, DocuChat AI is your personal assistant for document-based queries.

📝 Table of Contents
✨ Features

🚀 Quickstart

📁 Project Structure

💡 How It Works

🛠️ Configuration

🤝 Contributing

📄 License

✨ Features
Multi-Format Support: Easily upload and process .pdf, .docx, and .txt files.

Intelligent Chat: Ask questions in natural language and get precise answers based on the content of your documents.

Customizable Embeddings: Choose between OpenAI or local Sentence-Transformers for generating vector embeddings.

Efficient Knowledge Base: Uses ChromaDB as a local, fast, and lightweight vector store.

Clean & Responsive UI: Built with Streamlit for a simple, elegant user experience.

🚀 Quickstart
Follow these simple steps to get the application running on your local machine.

1. Clone the Repository
git clone https://github.com/Snehajindl24/DocuChatAI.git
cd DocuChatAI

2. Set up the Environment
Create a virtual environment and install the required packages.

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Configure API Key
Copy the example environment file and add your OpenAI API key.

cp .env.example .env

Now, open the newly created .env file and replace your_api_key_here with your actual key.

# .env
OPENAI_API_KEY=sk-proj-YOUR_API_KEY_HERE
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBED_MODEL=text-embedding-3-small

4. Run the App
Launch the Streamlit application.

streamlit run app.py

Your application should now be running in your browser at http://localhost:8501.

📁 Project Structure
The repository is organized into a clean and modular structure:

.
├── .env                 # Environment variables for API keys , i have not added mine here you can just copy .env.example
├── .env.example         # Template for .env file
├── .gitignore           # Files and directories to ignore
├── README.md            # You are here!
├── app.py               # Main Streamlit application
├── config.py            # Application configuration
├── requirements.txt     # Python dependencies
└── utils/
    ├── __init__.py
    ├── chunking.py      # Logic for splitting documents into chunks
    ├── docx_loader.py   # Loader for .docx files
    ├── embedding.py     # Embedding functions (OpenAI/local)
    ├── pdf_loader.py    # Loader for .pdf files
    ├── query.py         # Handles RAG logic and querying
    ├── text_loader.py   # Loader for .txt files
    └── vector_store.py  # ChromaDB functions

💡 How It Works
This application uses a Retrieval-Augmented Generation (RAG) framework, which works in a few simple steps:

Load Documents: You upload your files (.pdf, .docx, .txt).

Chunking: The app splits the documents into smaller, manageable pieces or "chunks."

Embedding: Each chunk is converted into a numerical vector representation (an "embedding").

Vector Store: These embeddings are stored in a vector database (ChromaDB) which acts as your knowledge base.

Query & Retrieval: When you ask a question, your query is also converted to a vector. The app then performs a similarity search to find the most relevant document chunks from the vector store.

Augmented Generation: The retrieved chunks are provided to a large language model (LLM) as context, allowing it to generate a precise, grounded answer to your question.

🛠️ Configuration
You can customize the application behavior by editing config.py or by using the sidebar controls in the app.

OPENAI_API_KEY: Your key for using OpenAI models.

OPENAI_CHAT_MODEL: The chat model to be used for generation (e.g., gpt-4o-mini).

OPENAI_EMBED_MODEL: The embedding model to be used (e.g., text-embedding-3-small).

🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.
