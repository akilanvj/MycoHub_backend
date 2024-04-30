import gzip
from Bio import SeqIO

# MgArd0001_A	ACAGCGT	ACGTACA
# MgArd0002	ACAGCGT	ACGTCAG
# MgArd0003	ACAGCGT	ACTAGCA
# MgArd0004	ACAGCGT	ACTCGTC
# MgArd0009	ACAGTAG	ACGTACA
# MgArd0010	ACAGTAG	ACGTCAG
# MgArd0011	ACAGTAG	ACTAGCA
# MgArd0012	ACAGTAG	ACTCGTC
# MgArd0001_B	ACAGCGC	ACGTACT

def read_fastq_gz(fastq_gz_file):
    with gzip.open(fastq_gz_file, "rt") as handle:
        for record in SeqIO.parse(handle, "fastq"):
            yield record

fastq_gz_file = "test/data/demultiplex_test2_R1.fq.gz"

for record in read_fastq_gz(fastq_gz_file):
    print("" + record.id+" ")
    print(record)
    # print("Sequence:", record.seq)
    # print("Quality scores:", record.letter_annotations["phred_quality"])

# def extract_barcodes(input_fastq, barcode_length, barcode_start):
#     barcode_counts = {}
#     with open(input_fastq, "r") as handle:
#         for record in SeqIO.parse(handle, "fastq"):
#             barcode = str(record.seq[barcode_start:barcode_start + barcode_length])
#             barcode_counts[barcode] = barcode_counts.get(barcode, 0) + 1
#     return barcode_counts
#
# input_fastq = "test/data/Assessment_datasets_its1_powerlaw/35sp/jeu1/ITS1/Powerlaw/Archive/35sp_Powerlaw-01_R1.fastq"
# barcode_length = 8  # Example barcode length
# barcode_start = 0   # Example barcode start position
#
# barcode_counts = extract_barcodes(input_fastq, barcode_length, barcode_start)
#
# # Print barcode counts
# for barcode, count in barcode_counts.items():
#     print(f"Barcode: {barcode}, Count: {count}")

