from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(docs, chunk_size=900, chunk_overlap=150):
    """
    Splits a list of LangChain Document objects into smaller chunks.
    
    Args:
        docs: List of Document objects to be split.
        chunk_size: Maximum number of characters per chunk.
        chunk_overlap: Number of characters to overlap between chunks.
        
    Returns:
        List of Document objects with chunked text.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(docs)
