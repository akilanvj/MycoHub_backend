import gzip


def extract_barcodes_from_fastq_gz(fastq_gz_file, barcode_length):
    barcode_sequence_pairs = []
    with gzip.open(fastq_gz_file, "rt") as handle:
        for line_num, line in enumerate(handle):
            print("Printing the data " + line.strip() + " Line _ number " + str(line_num))
            if line_num % 4 == 0:  # Header line
                header = line.strip().replace("@", "").split(" ")[0]
            elif line_num % 4 == 1:  # Sequence line
                sequence = line.strip()
                barcode = sequence[:barcode_length]
                last_sequence_chars = sequence[-sequence_length:]  # Extract last 'sequence_length' characters
                barcode_sequence_pairs.append((header, barcode, last_sequence_chars))
    return barcode_sequence_pairs


def pair_barcode_sequences(barcode_sequences_r1, barcode_sequences_r2):
    paired_barcode_sequences = []
    for header, barcode_r1 in barcode_sequences_r1.items():
        if header in barcode_sequences_r2:
            barcode_r2 = barcode_sequences_r2[header]
            paired_barcode_sequences.append((header, barcode_r1, barcode_r2))
    return paired_barcode_sequences


def pair_barcode_sequences_first(barcode_sequences_r1, barcode_sequences_r2):
    paired_barcode_sequences = []
    for header, barcode_r1 in barcode_sequences_r1.items():
        if header in barcode_sequences_r2:
            barcode_r2 = barcode_sequences_r2[header]
            paired_barcode_sequences.append((header, barcode_r1, barcode_r2))
    return paired_barcode_sequences


def pair_barcode_sequences(barcode_sequences_r1, barcode_sequences_r2):
    paired_barcode_sequences = []
    for header, barcode_r1 in barcode_sequences_r1.items():
        if header in barcode_sequences_r2:
            barcode_r2 = barcode_sequences_r2[header]
            # Check if both barcodes are valid (no N's and equal lengths)
            if "N" not in barcode_r1 and "N" not in barcode_r2 and len(barcode_r1) == len(barcode_r2):
                paired_barcode_sequences.append((header, barcode_r1, barcode_r2))
    return paired_barcode_sequences


def generate_barcode_sequence_file(data, output_file):
    with open(output_file, "w") as f:
        for header, barcode_r1, barcode_r2 in data:
            f.write(f"{header}\t{barcode_r1}\t{barcode_r2}\n")


# Read barcode sequences from R1 FASTQ.gz file
# fastq_gz_file_r1 = "data/35sp_Powerlaw-01_R1.fastq.gz"
# fastq_gz_file_r2 = "data/35sp_Powerlaw-01_R2.fastq.gz"

fastq_gz_file_r1 = "data/demultiplex_test2_R1.fq.gz"
fastq_gz_file_r2 = "data/demultiplex_test2_R2.fq.gz"

barcode_length_r1 = 7  # Example barcode length for R1
sequence_length = 7

barcode_sequences_r1 = extract_barcodes_from_fastq_gz(fastq_gz_file_r1, barcode_length_r1)
# print('BarCode Sequence 1')
# print(barcode_sequences_r1)

# Read barcode sequences from R2 FASTQ.gz file

barcode_length_r2 = 7  # Example barcode length for R2

barcode_sequences_r2 = extract_barcodes_from_fastq_gz(fastq_gz_file_r2, barcode_length_r2)
# print('BarCode Sequence 2')
# print(barcode_sequences_r2)

# Assuming you have barcode sequences from R1 and R2 stored as tuples
barcode_sequences_r1_tulpes = {header: barcode for header, barcode, _ in barcode_sequences_r1}
barcode_sequences_r2_tulpes = {header: barcode for header, _, barcode in barcode_sequences_r2}

# print(barcode_sequences_r2_tulpes)

# Pair barcode sequences from R1 and R2 tuples
paired_barcode_sequences = pair_barcode_sequences(barcode_sequences_r1_tulpes, barcode_sequences_r2_tulpes)

# Generate barcode sequence file
# output_file = "demultiplex_barcode.txt"
# output_file = "paired_barcode_sequences.txt"

output_file = "demultiplex_barcode.txt"
generate_barcode_sequence_file(paired_barcode_sequences, output_file)

print("Paired barcode sequence file generated:", output_file)
