import gzip
from Bio import SeqIO
import os


def fastq_gz_to_fasta(input_fastq_gz, output_fasta):
    with gzip.open(input_fastq_gz, "rt") as handle:
        with open(output_fasta, "w") as output_handle:
            for record in SeqIO.parse(handle, "fastq"):
                SeqIO.write(record, output_handle, "fasta")


def extract_base_name(file_path, file_type):
    base_name = os.path.basename(file_path)
    if file_type == 'full':
        return base_name
    elif file_type == 'name':
        return os.path.splitext(base_name)[0]
    elif file_type == 'extension':
        return os.path.splitext(base_name)[1]
    else:
        return None  # Return None for invalid file types


def extract_output_file_path(file_path):
    base_name = extract_base_name(file_path, "name")
    return extract_base_name(base_name, "name") + ".fasta"


input_fastq_gz = "35sp_Powerlaw-02_R1.fastq.gz"
output_file_name = extract_output_file_path(input_fastq_gz)
output_fasta = "output/" + output_file_name

fastq_gz_to_fasta(input_fastq_gz, output_fasta)
print(f"Conversion from {input_fastq_gz} to {output_fasta} complete.")
