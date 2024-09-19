import sys

# translation key between RNA codons and the resultant amino acid
codon_key = {
    "UUU": "F",
    "UUC": "F",
    "UUA": "L",
    "UUG": "L",
    "UCU": "S",
    "UCC": "S",
    "UCA": "S",
    "UCG": "S",
    "UAU": "Y",
    "UAC": "Y",
    "UAA": "*",
    "UAG": "*",
    "UGU": "C",
    "UGC": "C",
    "UGA": "*",
    "UGG": "W",
    "CUU": "L",
    "CUC": "L",
    "CUA": "L",
    "CUG": "L",
    "CCU": "P",
    "CCC": "P",
    "CCA": "P",
    "CCG": "P",
    "CAU": "H",
    "CAC": "H",
    "CAA": "Q",
    "CAG": "Q",
    "CGU": "R",
    "CGC": "R",
    "CGA": "R",
    "CGG": "R",
    "AUU": "I",
    "AUC": "I",
    "AUA": "I",
    "AUG": "M",
    "ACU": "T",
    "ACC": "T",
    "ACA": "T",
    "ACG": "T",
    "AAU": "N",
    "AAC": "N",
    "AAA": "K",
    "AAG": "K",
    "AGU": "S",
    "AGC": "S",
    "AGA": "R",
    "AGG": "R",
    "GUU": "V",
    "GUC": "V",
    "GUA": "V",
    "GUG": "V",
    "GCU": "A",
    "GCC": "A",
    "GCA": "A",
    "GCG": "A",
    "GAU": "D",
    "GAC": "D",
    "GAA": "E",
    "GAG": "E",
    "GGU": "G",
    "GGC": "G",
    "GGA": "G",
    "GGG": "G"
}

# preinitialized dictionary for each amino acid occuence, in the required order
amino_acid_occurences = {
    "A" : 0,
    "C" : 0,
    "D" : 0,
    "E" : 0,
    "F" : 0,
    "G" : 0,
    "H" : 0,
    "I" : 0,
    "K" : 0,
    "L" : 0,
    "M" : 0,
    "N" : 0,
    "P" : 0,
    "Q" : 0,
    "R" : 0,
    "S" : 0,
    "T" : 0,
    "V" : 0,
    "W" : 0,
    "Y" : 0
}

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

    codon_count = 0
    running_str = ''

    # Iterate through each line in the input file
    for line in in_file:
        # Iterate through each character in the line
        for c in line:
            # Check if the character is one of 'A', 'C', 'G', or 'U'
            if c in 'ACGU':
                
                running_str = ''.join((running_str, c))
                codon_count += 1

                # if we have reached 3 RNA letters, we have created a codon, so we decode with the chart we defined above
                if codon_count % 3 == 0:
                    amino_acid = codon_key[running_str]

                    running_str = ''

                    # ignore stop codons
                    if amino_acid == '*':
                        continue

                    # add this occurence to the dictionary of previous occurence counts
                    amino_acid_occurences[amino_acid] += 1

    first = True

    for key in amino_acid_occurences:
        if first:
            first = False
        else:
            # add commas between elements
            out_file.write(',')

        out_file.write(str(amino_acid_occurences[key]))
