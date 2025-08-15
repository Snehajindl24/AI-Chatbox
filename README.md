# DocuChat AI – Chat with your documents (RAG)

Upload PDFs/DOCX/TXT and ask questions. Uses LangChain + ChromaDB, OpenAI or local Sentence-Transformers embeddings.

## Quickstart
```bash
pip install -r requirements.txt
cp .env.example .env  # add your OPENAI_API_KEY
streamlit run app.py