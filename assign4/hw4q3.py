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

    best_match_right = {}
    best_match_left = {}

    lines = in_file.readlines()

    for line in lines:
        split_line = line.split()
        if len(split_line) != 3:
            print("Each line must have exactly three datapoints on it for this to be valid")
            sys.exit(1)
        
        try:
            align_len = int(split_line[1])
        except ValueError:
            print("Second element of line must be of integer type")
            sys.exit(1)

        left_read = split_line[0]
        right_read = split_line[2]

        if left_read in best_match_right:
            print("Duplicate specification of best match to the right")
            sys.exit(1)
        
        best_match_right[left_read] = (right_read, align_len)

        if right_read not in best_match_left:
            best_match_left[right_read] = (left_read, align_len)
        else:
            if align_len > best_match_left[right_read][1]:
                best_match_left[right_read] = (left_read, align_len)
            elif align_len == best_match_left[right_read][1]:
                # duplicate, therefore is no longer unique
                best_match_left[right_read] = (None, align_len)
    
    in_chain = set()
    not_first = set()

    # iterate once to find what the first parts of the chains are
    for read in best_match_right:
        bml_of_bmr = best_match_left[(best_match_right[read])[0]][0]
        if read == bml_of_bmr:
            # we have an unambiguous pair - store the dest read in a set to remind that it cannot be the first listed, since something else "points" to it
            not_first.add(best_match_right[read][0])
            # store the source read to know that it is used in a chain
            in_chain.add(read)

    
    used_reads = set()
    first = True

    keys = list(best_match_right.keys())
    keys.sort()

    # now go through the alphabetically ordered keys and follow heads of the chains to their end
    for key_r in keys:
        if key_r in used_reads:
            # we do not want to print the same key twice - this should already be covered by the other case but this is a sanity check at least
            continue
        elif key_r in not_first or key_r not in in_chain:
            # if this read is not in a chain, we do not even consider it,
            # if this read is not the first in the chain, we will get to it later
            continue

        if first:
            first = False
        else:
            out_file.write('\n')
        out_file.write(key_r)

        read = key_r

        while True:

            if read not in best_match_right:
                break

            bmr = best_match_right[read][0]
            bml_of_bmr = best_match_left[bmr][0]

            if bml_of_bmr != read:
                break

            used_reads.add(read)

            out_file.write('\n' + str(best_match_right[read][1]) + " ")
            out_file.write(bmr)

            read = bmr