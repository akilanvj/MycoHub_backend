import gzip
from Bio import SeqIO


def convert_fastq_to_fasta(input_fastq_gz, output_fasta):
    """
    Convert a fastq.gz file to a fasta file.

    :param input_fastq_gz: Path to the input fastq.gz file
    :param output_fasta: Path to the output fasta file
    """
    with gzip.open(input_fastq_gz, "rt") as fastq_handle:
        with open(output_fasta, "w") as fasta_handle:
            SeqIO.convert(fastq_handle, "fastq", fasta_handle, "fasta")
    print(f"Conversion complete: {input_fastq_gz} -> {output_fasta}")


# Example usage
input_fastq_gz = '35sp_Powerlaw-01_R1.fastq.gz'
output_fasta = 'output/35sp_Powerlaw-01_R1.fasta'
convert_fastq_to_fasta(input_fastq_gz, output_fasta)
