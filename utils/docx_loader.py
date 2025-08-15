import tempfile
from langchain_community.document_loaders import UnstructuredWordDocumentLoader

def load_docx(uploaded_file):
    # Save uploaded DOCX to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    loader = UnstructuredWordDocumentLoader(tmp_path)
    return loader.load()
