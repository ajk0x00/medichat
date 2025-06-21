import fitz  # PyMuPDF

def extract_text_from_pdf(filepath: str) -> str:
    """Extracts all text from a PDF file."""
    text = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()
    return text