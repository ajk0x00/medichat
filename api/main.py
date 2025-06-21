from fastapi import FastAPI, UploadFile

from utils.pdf_utils import extract_text_from_pdf

app = FastAPI()


@app.post("/upload")
async def read_root(file: UploadFile):
    with open(f"files/{file.filename}.txt", "wb") as f:
        if file.content_type == 'application/pdf':
            file_content = extract_text_from_pdf(f"files/{file.filename}")
        else:
            file_content = await file.read()
        f.write(file_content)
    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }