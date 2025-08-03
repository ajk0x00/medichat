import pymupdf4llm

def extract_text_from_pdf(filepath: str) -> str:
    return pymupdf4llm.to_markdown(filepath)
