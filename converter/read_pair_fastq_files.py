import gzip
from Bio import SeqIO
import gzip
from Bio import SeqIO
import random

# Define the file paths for R1 and R2 FASTQ files
input_r1_fastq_gz = "demultiplex_test2_R1.fq.gz"
input_r2_fastq_gz = "demultiplex_test2_R2.fq.gz"


def generate_barcodes(num_barcodes, barcode_length):
    bases = ['A', 'C', 'G', 'T']
    barcodes = []
    while len(barcodes) < num_barcodes:
        barcode = ''.join(random.choices(bases, k=barcode_length))
        if barcode not in barcodes:
            barcodes.append(barcode)
    return barcodes


# Define parameters
num_barcodes = 96
barcode_length = 8
output_merged_fastq = "output/merged.fastq"


def is_multiplexed(fastq_file):
    with open(fastq_file, "r") as f:
        # Read the first few lines to check for barcode or index sequences
        for _ in range(10):  # Read the first 10 records
            header = next(f).strip()  # Read sequence header
            if "+" in header:  # Check if the header contains a '+' symbol (common in FASTQ headers)
                parts = header.split("+")  # Split header by '+'
                if len(parts) > 1:  # Check if there are multiple parts
                    barcode = parts[1]  # Assume the second part is the barcode
                    if len(barcode) > 0:  # Check if the barcode is not empty
                        return True
    return False


# Example usage
fastq_file = "output/demultiplex_test2_R1.fasta"
if is_multiplexed(fastq_file):
    print("The FASTQ file is multiplexed.")
else:
    print("The FASTQ file is not multiplexed")

# Generate barcodes
barcodes = generate_barcodes(num_barcodes, barcode_length)

# Open output file for writing
with open(output_merged_fastq, "w") as output_handle:
    # Open input R1 FASTQ.gz file for reading
    with gzip.open(input_r1_fastq_gz, "rt") as handle_r1:
        # Open input R2 FASTQ.gz file for reading
        with gzip.open(input_r2_fastq_gz, "rt") as handle_r2:
            # Iterate over records in the R1 and R2 FASTQ.gz files simultaneously
            for record_r1, record_r2 in zip(SeqIO.parse(handle_r1, "fastq"), SeqIO.parse(handle_r2, "fastq")):
                # Select a random barcode
                barcode = random.choice(barcodes)
                # Prepend the barcode to the sequence and quality scores in both R1 and R2
                record_r1.seq = barcode + record_r1.seq
                record_r1.letter_annotations["phred_quality"] = [30] * len(barcode) + record_r1.letter_annotations[
                    "phred_quality"]
                record_r2.seq = barcode + record_r2.seq
                record_r2.letter_annotations["phred_quality"] = [30] * len(barcode) + record_r2.letter_annotations[
                    "phred_quality"]
                # Write the modified records to the output merged FASTQ file
                SeqIO.write(record_r1, output_handle, "fastq")
                SeqIO.write(record_r2, output_handle, "fastq")

print("Merged FASTQ file with barcodes generated:", output_merged_fastq)
