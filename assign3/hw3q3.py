def get_all_suffixes(line):
    suffix_list = []
    suffix_index = {}

    for i in range(len(line)):
        suffix = line[i:]
        suffix_list.append(suffix)
        suffix_index[suffix] = i

    return suffix_list, suffix_index

def build_suffix_array(line):

    suffix_array = []

    suffix_list, suffix_index = get_all_suffixes(line)
    suffix_list.sort()

    for suffix in suffix_list:
        suffix_array.append(suffix_index[suffix])
        
    return suffix_array

# this function borrowed mostly from CG_BWT_SimpleBuild.ipynb course notebook
def build_bw_indices_from_sa(line):
    suffix_array = build_suffix_array(line)

    bwt_indices = []

    for i in suffix_array:
        if i == 0:
            bwt_indices.append(len(line)-1)
        else:
            bwt_indices.append(i-1)
    
    return bwt_indices

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

    line = in_file.readline().strip()

    bwt_indices = build_bw_indices_from_sa(line)

    first = True
    for index in bwt_indices:
        if first:
            first = False
        else:
            out_file.write(' ')

        out_file.write(str(index))