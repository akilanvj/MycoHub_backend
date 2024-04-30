import gzip
from Bio import SeqIO


def filter_records(records):
    filtered_records = []
    for record in records:
        # Check if the sequence has any ambiguous bases (N)
        if 'N' not in record.seq:
            #print('Inside If block ')
            print(record)
            filtered_records.append(record)
        else:
            print("Ignored record: %s (Contains ambiguous bases)" % record.id)
    return filtered_records


# Open the compressed FASTQ.gz file using gzip.open() and pass the file handle to SeqIO.parse()
with gzip.open("demultiplex_test2_R2.fq.gz", "rt") as handle:
    records = SeqIO.parse(handle, "fastq")

    # Filter records
    filtered_records = filter_records(records)

    # Write the filtered records to a FASTA file
    count = SeqIO.write(filtered_records, "output/demultiplex_test2_R2.fasta", "fasta")
    print("Converted %i records" % count)
