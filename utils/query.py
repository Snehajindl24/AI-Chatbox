from utils.vector_store import similarity_search
from utils.embedding import get_chat_completion

def query_vector_store(user_query, collection_name="default_collection", embeddings=None, k=5):
    """
    Queries the vector store, retrieves similar documents, 
    and returns an AI-generated answer.

    Args:
        user_query (str): The user's question.
        collection_name (str): Name of the vector store collection.
        embeddings (object): The embedding function to use.
        k (int): Number of similar results to fetch.

    Returns:
        str: AI-generated answer.
    """
    # Retrieve relevant documents
    docs = similarity_search(user_query, collection_name=collection_name, embeddings=embeddings, k=k)

    # Combine document content for the prompt
    context_text = "\n\n".join([doc.page_content for doc in docs])

    # Prepare chat messages
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant that answers questions based on provided context."},
        {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {user_query}"}
    ]

    # Get AI-generated response
    answer = get_chat_completion(messages)
    return answer
