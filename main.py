import hashlib
import logging
import math
import os
from datetime import datetime

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from redis import Redis
from rq import Queue

UPLOAD_FOLDER = "uploads"
# Maximum allowed file size in bytes (change this to your desired limit)
MAX_FILE_SIZE = 100 * 1024 * 1024


def convert_bytes_to_mb(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def generate_timestamp_random():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_file_metadata(upload_file: UploadFile):
    file_name = upload_file.filename
    file_size = len(upload_file.file.read())
    mime_type = upload_file.content_type
    upload_file.file.seek(0)
    return file_name, file_size, mime_type


def calculate_hash(data):
    return hashlib.sha256(data).hexdigest()


def file_custom_path(file):
    check_path(UPLOAD_FOLDER)
    folder_name = generate_timestamp_random()
    upload_folder = os.path.join(UPLOAD_FOLDER, folder_name)
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    return file_path


def process_file(file_path, file_hash):
    print(f"Processing file: {file_path}, File Hash: {file_hash}")


class FileUploader:
    def __init__(self, app: FastAPI):
        self.app = app

    def register_routes(self):
        @self.app.get("/health")
        async def health_check():
            logging.info("Health check is successful")
            return {"status": True, "health_status": True}

        @self.app.get("/files/all")
        async def list_uploaded_files():
            files = []
            for folder in os.listdir(UPLOAD_FOLDER):
                folder_path = os.path.join(UPLOAD_FOLDER, folder)
                if os.path.isdir(folder_path):
                    for file_name in os.listdir(folder_path):
                        files.append({"filename": file_name, "folder": folder})
            return files

        @self.app.post("/upload/")
        async def upload_file(file: UploadFile = File(...)):
            try:
                file_path = file_custom_path(file)
                file_name, file_size, mime_type = get_file_metadata(file)
                with open(file_path, "wb") as f:
                    # Iterate over the file chunks and write them to disk
                    while chunk := await file.read(1024):  # Read 1KB chunks
                        f.write(chunk)
                file_size = os.path.getsize(file_path)
                mime_type = file.content_type
                # Fetch file metadata
                file_metadata = {
                    "filename": file_name,
                    "content_type": mime_type,
                    "file_size": convert_bytes_to_mb(file_size)
                }
                logging.info(f"File uploaded successfully: {file_metadata}")
                file_hash = ''
                with open(file_path, "rb") as image_file:
                    file_data = image_file.read()
                    file_hash = calculate_hash(file_data)
                    logging.info(f"File hash: {file_hash}")
                # Enqueue file for processing
                queue.enqueue(process_file, file_path, file_hash)

                return JSONResponse(content={"status": "success", "code": 200, "message": "File uploaded successfully",
                                             "metadata": file_metadata})
            except Exception as e:
                logging.exception("An error occurred while uploading the file", e)
                return JSONResponse(content={"status": "error", "code": 500, "error": str(e)})


app = FastAPI()
# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:9000",  # Example: frontend running on different port
    "http://127.0.0.1:9000",
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_conn = Redis(password='eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81')
queue = Queue(connection=redis_conn)
uploader = FileUploader(app)
uploader.register_routes()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level='info')
