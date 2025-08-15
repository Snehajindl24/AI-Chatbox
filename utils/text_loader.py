import tempfile
from langchain_community.document_loaders import TextLoader

def load_text(uploaded_file):  # <- changed from load_txt to load_text
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    loader = TextLoader(tmp_path, encoding="utf-8")
    return loader.load()
