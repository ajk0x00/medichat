import api.utils.llm as llm

from fastapi import FastAPI, UploadFile

from api.models import Question
from api.utils.pdf_utils import extract_text_from_pdf
from api.utils.vector_db import add_text_to_vector_db, query_vector_db
from dotenv import load_dotenv
print('starting the application')

load_dotenv()

llm.init()
app = FastAPI()


@app.post("/upload")
async def read_root(file: UploadFile):
    if file.content_type == 'application/pdf':
        with open(f"files/{file.filename}", "wb") as f:
            content = await file.read()
            f.write(content)
        file_content = extract_text_from_pdf(f"files/{file.filename}")
    else:
        file_content = await file.read()
    add_text_to_vector_db(file_content)
    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }

@app.post("/ask")
def ask(query: Question):
    print(f"Received question: {query.question}")
    results = query_vector_db(query.question)
    print(f"Retrieved results: {results}")
    response = llm.summarize(query.question, results)
    return {    
        "results": response
    }
