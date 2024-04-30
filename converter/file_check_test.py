import re


def is_fungi_sequence(sequence):
    # Define a regular expression pattern for a typical ITS sequence in fungi
    pattern = r"CGATAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATT"

    # Use regular expression search to find matches
    match = re.search(pattern, sequence)

    # If a match is found, consider it as a fungi sequence
    if match:
        return True
    else:
        return False


# Example sequence
sequence = "CGATAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTACCGCGACCTGTTGTTGAACTCGCTGTGGCCGCTTGGTCACCCTCCTTTCC"
if is_fungi_sequence(sequence):
    print("The sequence belongs to fungi.")
else:
    print("The sequence does not belong to fungi.")
