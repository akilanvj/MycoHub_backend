import gzip


def extract_barcode_sequence_from_fastq_gz(fastq_gz_file, barcode_length, sequence_length):
    barcode_sequence_pairs = []
    with gzip.open(fastq_gz_file, "rt") as handle:
        for line_num, line in enumerate(handle):
            if line_num % 4 == 0:  # Header line
                header = line.strip().replace("@", "").split(" ")[0]
            elif line_num % 4 == 1:  # Sequence line
                sequence = line.strip()
                barcode = sequence[:barcode_length]
                last_sequence_chars = sequence[-sequence_length:]  # Extract last 'sequence_length' characters
                barcode_sequence_pairs.append((header, barcode, last_sequence_chars))
    return barcode_sequence_pairs


def generate_barcode_sequence_file(data, output_file):
    with open(output_file, "w") as f:
        for identifier, barcode, sequence in data:
            f.write(f"{identifier}\t{barcode}\t{sequence}\n")


fastq_gz_file = "data/demultiplex_test2_R1.fq.gz"
barcode_length = 7  # Example barcode length
sequence_length = 7  # Example sequence length

# Extract barcode and sequence pairs from the FASTQ.gz file
barcode_sequence_pairs = extract_barcode_sequence_from_fastq_gz(fastq_gz_file, barcode_length, sequence_length)

# Generate barcode sequence file
output_file = "output/barcode_sequences_r1_file.txt"
generate_barcode_sequence_file(barcode_sequence_pairs, output_file)

print("Barcode sequence file generated:", output_file)
