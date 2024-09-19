# Import the sys module to access command-line arguments
import sys

# This module is for your reference to understand the usage
if len(sys.argv) != 3:
    print("Usage: python3 hw1q1b.py <input_file> <output_file>")
    sys.exit(1)

# Assign the input and output filenames from command-line arguments
input_file = sys.argv[1] # First argument: input filename
output_file = sys.argv[2] # Second argument: output filename

# Open input file
with open(input_file, 'r') as in_file:

    substring_dict = {}
    current_substring_list = []

    current_best_substring = ''
    current_best_entry = [0, []] 

    index = 0

    # Iterate through each line in the input file
    for line in in_file:
        # Iterate through each character in the line
        for c in line:
            # Check if the character is one of 'A', 'C', 'G', or 'T'
            if c in 'ACGT':

                # add the character to the running substring
                current_substring_list.append(c)

                # if we have not yet accumulated 6 characters in the string, then we keep going
                if index < 5:
                    index += 1
                    continue
                # if we have more than 6 characters, we want to keep only 6 in the running string
                elif index >= 6:
                    current_substring_list.pop(0)

                current_substring = ''.join(current_substring_list)

                # initialize the dict with the current substring if it has not been seen before
                if current_substring not in substring_dict:
                    substring_dict[current_substring] = []
                    substring_dict[current_substring].append(0)
                    substring_dict[current_substring].append([])

                substring_entry = substring_dict[current_substring]

                # marks that this substring has occured once more, at this index
                substring_entry[0] += 1
                substring_entry[1].append(index - 5)                    

                # check if we have a new best choice for most common substring, breaking ties by lexicographic order
                if substring_entry[0] >= current_best_entry[0]:
                    if current_best_entry[0] == 0 or substring_entry[0] > current_best_entry[0] or current_substring < current_best_substring:
                        current_best_substring = current_substring
                        current_best_entry = substring_entry
                
                index += 1

# Open output file
with open(output_file, 'w') as out_file:
    first = True
    for c in current_best_entry[1]:
        if first:
            first = False
        else:
            # add commas between every element
            out_file.write(',')

        out_file.write(str(c))
