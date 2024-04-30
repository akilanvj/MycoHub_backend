import gzip


def extract_barcodes_from_fastq_gz(fastq_gz_file, barcode_length):
    barcode_sequences = {}
    with gzip.open(fastq_gz_file, "rt") as handle:
        for line_num, line in enumerate(handle):
            if line_num % 4 == 0:  # Header line
                header = line.strip()
            elif line_num % 4 == 1:  # Sequence line
                sequence = line.strip()
                barcode = sequence[:barcode_length]
                barcode_sequences[header] = barcode
    return barcode_sequences


def pair_barcodes(barcode_sequences_r1, barcode_sequences_r2):
    paired_barcodes = []
    for header, barcode_r1 in barcode_sequences_r1.items():
        if header in barcode_sequences_r2:
            barcode_r2 = barcode_sequences_r2[header]
            paired_barcodes.append((barcode_r1, barcode_r2))
    return paired_barcodes


def write_barcode_file(barcode_pairs, output_file):
    with open(output_file, "w") as f:
        for barcode_r1, barcode_r2 in barcode_pairs:
            f.write(f"{barcode_r1}\t{barcode_r2}\n")


# Parameters
fastq_gz_file_r1 = "data/demultiplex_test2_R1.fq.gz"
fastq_gz_file_r2 = "data/demultiplex_test2_R2.fq.gz"
barcode_length = 8  # Example barcode length
output_file = "paired_barcode_file.txt"

# Extract barcode sequences from R1 and R2 FASTQ.gz files
barcode_sequences_r1 = extract_barcodes_from_fastq_gz(fastq_gz_file_r1, barcode_length)
barcode_sequences_r2 = extract_barcodes_from_fastq_gz(fastq_gz_file_r2, barcode_length)

# Pair barcode sequences from R1 and R2
paired_barcodes = pair_barcodes(barcode_sequences_r1, barcode_sequences_r2)

# Write paired barcode sequences to a file
write_barcode_file(paired_barcodes, output_file)

print("Paired barcode file generated:", output_file)
