import os
import shutil
from langchain_community.vectorstores import Chroma
from utils.embedding import get_embedding_function

VECTOR_STORE_DIR = "vector_store"

def get_chroma(collection_name="default_collection", embeddings=None):
    """
    Initializes or loads a Chroma vector store.
    """
    if embeddings is None:
        raise ValueError("Embedding function is required.")
    
    return Chroma(
        collection_name=collection_name,
        persist_directory=VECTOR_STORE_DIR,
        embedding_function=embeddings
    )

def similarity_search(query, collection_name="default_collection", embeddings=None, k=5):
    """
    Performs a similarity search on the vector store.
    """
    if embeddings is None:
        raise ValueError("Embedding function is required.")
    db = get_chroma(collection_name, embeddings)
    return db.similarity_search(query, k=k)

def clear_vector_store(vectordb):
    """
    Deletes the local vector store to reset the knowledge base.
    """
    # Attempt to close the database client if it exists
    try:
        vectordb.delete_collection()
        vectordb._client.clear_system_cache()
    except Exception as e:
        print(f"Error while clearing ChromaDB collection: {e}")
        
    # Now, attempt to delete the directory
    if os.path.exists(VECTOR_STORE_DIR):
        try:
            shutil.rmtree(VECTOR_STORE_DIR)
        except OSError as e:
            print(f"Error during directory deletion: {e.strerror}")

