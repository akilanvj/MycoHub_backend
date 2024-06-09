import hashlib
import os
from datetime import datetime

from fastapi import UploadFile

from utils.file_type import FileType


class FileUtils:
    @staticmethod
    def get_file_metadata(upload_file: UploadFile):
        file_name = upload_file.filename
        file_size = len(upload_file.file.read())
        mime_type = upload_file.content_type
        upload_file.file.seek(0)
        return file_name, file_size, mime_type

    @staticmethod
    def calculate_hash(data):
        return hashlib.sha256(data).hexdigest()

    # Function to generate timestamped folder name
    @staticmethod
    def generate_timestamp_random():
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    @staticmethod
    def check_path(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def extract_base_name(file_path, file_type):
        base_name = os.path.basename(file_path)
        if file_type == 'full':
            return base_name
        elif file_type == 'name':
            return os.path.splitext(base_name)[0]
        elif file_type == 'extension':
            return os.path.splitext(base_name)[1]
        elif file_type == 'dir':
            return os.path.dirname(file_path)
        else:
            return None



    @staticmethod
    def convert_bytes_to_mb(size_in_bytes):
        return size_in_bytes / 1024 / 1024

    @staticmethod
    def is_directory_exists(directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    @staticmethod
    def extract_output_file_path(file_path):
        base_name = FileUtils.extract_base_name(file_path, "name")
        return FileUtils.extract_base_name(base_name, "name") + "." + str(FileType.FASTA.value)
