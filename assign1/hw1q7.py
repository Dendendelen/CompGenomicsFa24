# Import the sys module to access command-line arguments
import sys

if len(sys.argv) != 3:
    print("Usage: python3 hw1q1b.py <input_file> <output_file>")
    sys.exit(1)

# Assign the input and output filenames from command-line arguments
input_file = sys.argv[1] # First argument: input filename
output_file = sys.argv[2] # Second argument: output filename

# Open both input file
with open(input_file, 'r') as in_file:

    first = True

    first_string = ''
    second_string = ''

    # Iterate through each line in the input file
    for line in in_file:
        # Iterate through each character in the line
        if first:
            for c in line:
                first_string = ''.join((first_string, c))
            first = False
        else: 
            # since we are allowed to assume inputs are well formatted, then any line that is not the first must be only the second
            for c in line:
                second_string = ''.join((second_string, c)) 

differences = 0

# iterate through the strings in lockstep with the zip function, checking letter-by-letter differences
for i,j in zip(first_string, second_string):
    if i != j:
        differences += 1
    
with open(output_file, 'w') as out_file:
    out_file.write(str(differences))