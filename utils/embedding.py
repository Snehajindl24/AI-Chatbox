import os
from openai import OpenAI

# -------------------------------
# Get embedding function
# -------------------------------
def get_embedding_function(provider="openai", openai_embed_model=None):
    """
    Returns an embedding function depending on the provider.
    """
    if provider.lower() == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OpenAI API key missing. Please set OPENAI_API_KEY in your .env file.")
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model=openai_embed_model or os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small"))
    else:
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        except ImportError:
            raise RuntimeError("HuggingFace sentence-transformers not installed. Install with `pip install sentence-transformers`")

# -------------------------------
# Get chat completion
# -------------------------------
def get_chat_completion(messages, model=None):
    """
    Generate a chat completion using OpenAI API.
    
    Args:
        messages (list): [{"role": "system", "content": "You are a helpful assistant."},
                          {"role": "user", "content": "Hello!"}]
        model (str): Chat model (defaults to env var)
    
    Returns:
        str: Model's reply
    """
    if model is None:
        model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OpenAI API key missing. Please set it in your .env file.")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content
