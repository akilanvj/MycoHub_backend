import os
from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


class FileUploader:
    def __init__(self, app: FastAPI):
        self.app = app

    def register_routes(self):
        @self.app.post("/uploadFiles/")
        async def upload_multiple_files(files: List[UploadFile] = File(...)):
            try:
                print('Printing the uploaded files - Starts Here')
                for file in files:
                    print(file)
                print('Printing the uploaded files - Ends Here')
                for file in files:
                    # Check if the file has a ".gz" extension
                    if not file.filename.endswith(".gz"):
                        return JSONResponse(status_code=400,
                                            content={"status": "error", "code": 400,
                                                     "detail": f"Only .gz files are allowed, but got {file.filename}"})
                    check_path('../helpers/uploads')
                    # Open a new file in "wb" mode (write binary)
                    with open(f"uploads/{file.filename}", "wb") as f:
                        # Iterate over the file chunks and write them to disk
                        while chunk := await file.read(1024):  # Read 1KB chunks
                            f.write(chunk)

                    # Fetch file metadata
                    file_metadata = {
                        "filename": file.filename,
                        "content_type": file.content_type,
                        "file_size": f.tell()  # Get the file size using file.tell()
                    }

                return JSONResponse(
                    content={"status": "success", "code": 200, "message": "Files uploaded successfully",
                             "metadata": file_metadata})
            except Exception as e:
                print('Exception occurred')
                print(str(e))
                return JSONResponse(content={"status": "error", "code": 500, "error": str(e)})

        @self.app.post("/upload/")
        async def upload_file(file: UploadFile = File(...)):
            try:
                # Check if the file has a ".gz" extension
                if not file.filename.endswith(".gz"):
                    return JSONResponse(status_code=400, content={"status": "error", "code": 400,
                                                                  "detail": "Only .gz files are allowed"})

                check_path('../helpers/uploads')
                # Open a new file in "wb" mode (write binary)
                with open(f"uploads/{file.filename}", "wb") as f:
                    # Iterate over the file chunks and write them to disk
                    while chunk := await file.read(1024):  # Read 1KB chunks
                        f.write(chunk)
                return JSONResponse(
                    content={"status": "success", "code": 200, "message": "File uploaded successfully"})
            except Exception as e:
                print('Exception occurred')
                print(str(e))
                return JSONResponse(content={"status": "error", "code": 500, "error": str(e)})


app = FastAPI()
uploader = FileUploader(app)
uploader.register_routes()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level='info')
