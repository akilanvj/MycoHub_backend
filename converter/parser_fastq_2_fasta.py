from utils.file_parser import FileParser
from utils.file_utils import FileUtils

input_fastq_gz = "data/35sp_Powerlaw-01_R1.fastq.gz"

output_fasta = FileParser.fastq_gz_to_fasta(input_fastq_gz)
print(f"Conversion from \"{FileUtils.extract_base_name(input_fastq_gz, 'full')}\" to \"{output_fasta}\" completed.")
