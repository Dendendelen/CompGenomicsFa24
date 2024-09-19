# Import the sys module to access command-line arguments
import sys

# global list of palindromes
list_of_palindromes = []

# helper function to return complements of DNA bases
def complement_of(c):
    if c == 'A':
        return 'T'
    if c == 'T':
        return 'A'
    if c == 'G':
        return 'C'
    if c == 'C':
        return 'G'

    # error condition
    sys.exit(1)
    return

# recursive function which gets palindromes of a particular length, and all lengths below it by calling itself
def palindrome_of_length(length, out_file):

    # align to the even, no odd palindromes can exist
    if length % 2 != 0:
        length -= 1

    # base case
    if length <= 0:
        return ['']

    # get all palindromes that are 2 shorter than the biggest ones we want
    old_palindromes = palindrome_of_length(length-2, out_file)

    palindromes = []

    for c in 'ACGT':
        for old in old_palindromes:
            # add every possible beginning and ending combo to all previous palindromes, to create ones of size 'length'
            out = ''.join((c, old, complement_of(c)))
            palindromes.append(out)
            # add all the new palindromes we have created to the global list
            list_of_palindromes.append(out)

    # send up the current length's palindromes for recursion
    return palindromes

if len(sys.argv) != 3:
    print("Usage: python3 hw1q1b.py <input_file> <output_file>")
    sys.exit(1)

# Assign the input and output filenames from command-line arguments
input_file = sys.argv[1] # First argument: input filename
output_file = sys.argv[2] # Second argument: output filename

# Open both input and output files - input file for reading and output file for writing
with open(input_file, 'r') as in_file, open(output_file, 'w') as out_file:

    digit_list = []    

    # Iterate through each line in the input file
    for line in in_file:
        # Iterate through each character in the line
        for c in line:
            # Check if the character is a digit
            if c in '0123456789':                
                digit_list.append(c)

    digit_str = ''.join(digit_list)
    value = int(digit_str)

    # recursively get all palindromes up to our length into the list, then sort it lexicographically
    palindrome_of_length(value, out_file)
    list_of_palindromes.sort()

    first = True

    for palindrome in list_of_palindromes:
        if first:
            first = False
        else:
            # line break between elements
            out_file.write('\n')

        out_file.write(palindrome)
                