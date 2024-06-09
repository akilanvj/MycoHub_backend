import gzip
import logging
import os

from Bio import SeqIO

from utils.file_type import FileType
from utils.file_utils import FileUtils

UPLOAD_FOLDER_PATH = "uploads"


class FileParser:
    @staticmethod
    def fastq_gz_to_fasta(input_fastq_gz):
        logging.info("Processing the file: \"{0}\"".format(FileUtils.extract_base_name(input_fastq_gz, "full")))
        output_file_name = FileUtils.extract_output_file_path(input_fastq_gz)
        output_folder_path = os.path.join(FileUtils.extract_base_name(input_fastq_gz, "dir"), "processed")
        FileUtils.is_directory_exists(output_folder_path)
        print("Output Folder Path -> ", output_folder_path)
        print("Output File Name -> ", output_file_name)
        full_path = os.path.join(output_folder_path, output_file_name)
        print("Full File Path -> ", full_path)
        with gzip.open(input_fastq_gz, "rt") as handle:
            with open(full_path, "w") as output_handle:
                SeqIO.convert(handle, FileType.FASTQ.value, output_handle, FileType.FASTA.value)
                return full_path
                # for record in SeqIO.parse(handle, FileType.FASTQ.value):
                #     SeqIO.write(record, output_handle, FileType.FASTA.value)
                #     return full_path
