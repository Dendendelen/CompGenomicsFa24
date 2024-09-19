import numpy as np

# function for handling FASTA, provided in https://nbviewer.org/github/BenLangmead/comp-genomics-class/blob/master/notebooks/FASTA.ipynb
def parse_fasta(fh):
    fa = {}
    current_short_name = None
    # Part 1: compile list of lines per sequence
    for ln in fh:
        if ln[0] == '>':
            # new name line; remember current sequence's short name
            long_name = ln[1:].rstrip()
            current_short_name = long_name.split()[0]
            fa[current_short_name] = []
        else:
            # append nucleotides to current sequence
            fa[current_short_name].append(ln.rstrip())
    # Part 2: join lists into strings
    for short_name, nuc_list in fa.items():
        # join this sequence's lines into one long string
        fa[short_name] = ''.join(nuc_list)
    return fa

# function to make a k-mer index from a string
def make_kmer_index(in_string, k):

    # set up dict
    kmer_dict = {}
    running_string_list = []
    index = 0

    for c in in_string:
        running_string_list.append(c)
        if len(running_string_list) < k:
            # allow us to get to k elements
            index += 1
            continue
        elif len(running_string_list) > k:
            # make sure we have only k elements
            running_string_list.pop(0)
        
        # forge the k characters into one running string
        running_string = ''.join(running_string_list)

        # preinitialize dict entry
        if running_string not in kmer_dict:
            kmer_dict[running_string] = []

        # add new index of occurence
        kmer_dict[running_string].append(index-k+1)

        index += 1

    return kmer_dict


# Import the sys module to access command-line arguments
import sys

# This module is for your reference to understand the usage
if len(sys.argv) != 4:
    print("Usage: python3 hw1q1b.py <input_file> <k_file> <output_file>")
    sys.exit(1)

# Assign the input and output filenames from command-line arguments
input_file = sys.argv[1] # First argument: input filename
k_value_file = sys.argv[2] # Second argument: k-source filename
output_file = sys.argv[3] # Third argument: output filename

# Open both input and output files - input file for reading and output file for writing
with open(input_file, 'r') as in_file, open(k_value_file, 'r') as k_file, open(output_file, 'w') as out_file:

    # read k from k file
    k = int(k_file.readline().strip())

    # parse FASTA from input file
    reads = parse_fasta(in_file)

    for key in reads:
        # add new k-mer index for the FASTA sequence
        kmer_index = make_kmer_index(reads[key], k)

        # the instructions give no insight on what to do with FASTA files with multiple sequences, so we just choose the first in that case
        break

    num_keys = 0
    num_one_occurences = 0

    for key in kmer_index:
        # count up key number - all are unique by property of dict
        num_keys += 1

        # count up those with only one occurence, i.e. size of 1 in the corresponding list
        if len(kmer_index[key]) <= 1:
            num_one_occurences += 1

    out_file.write(str(num_keys) + ' ' + str(num_one_occurences))




    