import numpy as np

# functions for handling FASTQ, provided in https://nbviewer.org/github/BenLangmead/comp-genomics-class/blob/master/notebooks/FASTQ.ipynb
def parse_fastq(fh):
    """ Parse reads from a FASTQ filehandle.  For each read, we
        return a name, nucleotide-string, quality-string triple. """
    reads = []
    while True:
        first_line = fh.readline()
        if len(first_line) == 0:
            break  # end of file
        name = first_line[1:].rstrip()
        seq = fh.readline().rstrip()
        fh.readline()  # ignore line starting with +
        qual = fh.readline().rstrip()
        reads.append((name, seq, qual))
    return reads

def phred33_to_q(qual):
  """ Turn Phred+33 ASCII-encoded quality into Phred-scaled integer """
  return ord(qual)-33

def q_to_phred33(Q):
  """ Turn Phred-scaled integer into Phred+33 ASCII-encoded quality """
  return chr(Q + 33)

def q_to_p(Q):
  """ Turn Phred-scaled integer into error probability """
  return 10.0 ** (-0.1 * Q)

def p_to_q(p):
  """ Turn error probability into Phred-scaled integer """
  import math
  return int(round(-10.0 * math.log10(p)))


def non_nucleotide_letter(c):
    if c in "AGCTacgt":
        return 0
    return 1

# Import the sys module to access command-line arguments
import sys

# This module is for your reference to understand the usage
if len(sys.argv) != 3:
    print("Usage: python3 hw1q1b.py <input_file> <output_file>")
    sys.exit(1)

# Assign the input and output filenames from command-line arguments
input_file = sys.argv[1] # First argument: input filename
output_file = sys.argv[2] # Second argument: output filename

# Open both input and output files - input file for reading and output file for writing
with open(input_file, 'r') as in_file, open(output_file, 'w') as out_file:

    # parse FASTQ from input file
    reads = parse_fastq(in_file)

    read_number = 1

    best_read = -1
    best_read_count = -1

    worst_read = -1
    worst_read_count = -1

    total_qualities_over_30 = 0
    total_qualities_under_10 = 0

    total_non_agtc_letters = 0

    for read in reads:
        names, nucleotides, qualities = read
        q_string = list(map(phred33_to_q, qualities))
        
        q_array = np.asarray(q_string)
        sum_quality = np.sum(q_array)

        if sum_quality > best_read_count:
            best_read = read_number
            best_read_count = sum_quality
        
        if sum_quality < worst_read_count or worst_read_count == -1:
            worst_read = read_number
            worst_read_count = sum_quality

        quality_over_30 = np.sum(q_array >= 30)
        total_qualities_over_30 += quality_over_30

        quality_below_10 = np.sum(q_array < 10)
        total_qualities_under_10 = quality_below_10

        total_non_agtc_letters += sum(list(map(non_nucleotide_letter, nucleotides)))

        read_number += 1

    out_file.write(str(worst_read) + ' ' + str(best_read) + ' ' + str(total_qualities_under_10) + ' ' + str(total_qualities_over_30) + ' ' + str(total_non_agtc_letters))




    