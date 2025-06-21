from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.post("/upload")
async def read_root(file: UploadFile):
    file_content = await file.read()
    with open(f"files/{file.filename}", "wb") as f:
        f.write(file_content)
    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }