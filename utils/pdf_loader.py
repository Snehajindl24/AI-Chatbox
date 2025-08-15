import tempfile
from langchain_community.document_loaders import PyPDFLoader

def load_pdf(uploaded_file):
    # Save uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    loader = PyPDFLoader(tmp_path)
    return loader.load()
