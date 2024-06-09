from fastapi import FastAPI, File, UploadFile, HTTPException
from rq import Queue
from redis import Redis
from datetime import datetime
import os
import shutil

# Maximum allowed file size in bytes (change this to your desired limit)
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

app = FastAPI()
redis_conn = Redis(password='eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81')
queue = Queue(connection=redis_conn)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Function to generate timestamped folder name
def generate_folder_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# Worker function to process file
def process_file(filename):
    # Placeholder processing logic
    # You can replace this with your actual processing logic
    print("Processing file:", filename)
    # Simulating processing delay
    import time
    time.sleep(5)


# Endpoint for file upload
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        folder_name = generate_folder_name()
        upload_folder = os.path.join(UPLOAD_FOLDER, folder_name)
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # Enqueue file for processing
        queue.enqueue(process_file, file.filename)
        # Set initial status of the file in Redis to "pending"
        redis_conn.set(f"{file.filename}_status", "pending")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"filename": file.filename, "folder": folder_name}


# Endpoint to get the status of a file
@app.get("/status/{filename}")
async def get_file_status(filename: str):
    status = redis_conn.get(f"{filename}_status")
    if status is None:
        raise HTTPException(status_code=404, detail="File not found")
    return {"filename": filename, "status": status.decode()}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
