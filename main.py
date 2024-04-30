from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from starlette.responses import FileResponse
import shutil
import os
from datetime import datetime
from rq import Queue
from redis import Redis

app = FastAPI()
redis_conn = Redis(password='eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81')
queue = Queue(connection=redis_conn)


# Function to generate timestamped folder name
def generate_folder_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# Worker function to process file uploads
def process_file(filename):
    # Here, you can implement any processing logic
    # For now, let's just print the filename
    print("Processing file:", filename)


UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Endpoint for file upload
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    folder_name = generate_folder_name()
    try:

        upload_folder = os.path.join("uploads", folder_name)
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            # Enqueue file for processing
            queue.enqueue(process_file, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": 200, "message": "File uploaded successfully and queued for processing",
            "filename": os.path.join("uploads", folder_name, file.filename)}


# Endpoint for file download
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, media_type="application/octet-stream", filename=filename)


# Endpoint for file download
@app.get("/download/{folder}/{filename}")
async def download_file(folder: str, filename: str):
    file_path = os.path.join("uploads", folder, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, media_type="application/octet-stream", filename=filename)


# Endpoint to list all uploaded files
@app.get("/files/")
async def list_uploaded_files():
    files = []
    for folder in os.listdir("uploads"):
        folder_path = os.path.join("uploads", folder)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                files.append({"filename": file_name, "folder": folder})
    return files


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
