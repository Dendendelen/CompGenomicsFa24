def get_all_suffixes(line):
    suffix_list = []
    suffix_index = {}

    for i in range(len(line)):
        suffix = line[i:]
        suffix_list.append(suffix)
        suffix_index[suffix] = i

    return suffix_list, suffix_index

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

    suffix_list, suffix_index = get_all_suffixes(line)

    suffix_list.sort()

    first = True
    for suffix in suffix_list:
        if first:
            first = False
        else:
            out_file.write(' ')
        
        out_file.write(str(suffix_index[suffix]))
