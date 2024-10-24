# Import the sys module to access command-line arguments
import sys
import numpy as np

# the below is mostly taken from the CG_kEditDp course notebook:

# Assume x is the string labeling rows of the matrix and y is the
# string labeling the columns
def trace(D, x, y):
    ''' Backtrace edit-distance matrix D for strings x and y '''
    i, j = len(x), len(y)
    xscript = []
    while i > 0:
        diag, vert, horz = sys.maxsize, sys.maxsize, sys.maxsize
        delt = None
        if i > 0 and j > 0:
            delt = 0 if x[i-1] != y[j-1] else 1
            diag = D[i-1, j-1] + delt
        if i > 0:
            vert = D[i-1, j] + 1
        if j > 0:
            horz = D[i, j-1] + 1
        if diag >= vert and diag >= horz:
            # diagonal was best
            xscript.append('R' if delt == 1 else 'M')
            i -= 1; j -= 1
        elif vert >= horz:
            # vertical was best; this is an insertion in x w/r/t y
            xscript.append('I')
            i -= 1
        else:
            # horizontal was best
            xscript.append('D')
            j -= 1
    # j = offset of the first (leftmost) character of t involved in the
    # alignment
    return j, (''.join(xscript))[::-1] # reverse and string-ize

def kEditDp(p, t):
    ''' Find and return the alignment of p to a substring of t with the
        most matches.  We return the matching value (1 for each match, 0 otherwise), the offset of the
        substring aligned to, and the edit transcript.  If multiple
        alignments tie for best, we report the leftmost. '''
    D = np.zeros((len(p)+1, len(t)+1), dtype=int)
    # Note: First row gets zeros.  First column initialized as usual.
    D[1:, 0] = 0
    for i in range(1, len(p)+1):
        for j in range(1, len(t)+1):
            delt = 1 if p[i-1] == t[j-1] else 0
            D[i, j] = max(D[i-1, j-1] + delt, D[i-1, j], D[i, j-1], 0)
    # Find maximum alignment value in last row
    mnJ, mn = None, -1
    for j in range(len(t)+1):
        if D[len(p), j] > mn:
            mnJ, mn = j, D[len(p), j]
    # Backtrace; note: stops as soon as it gets to first row
    off, xcript = trace(D, p, t[:mnJ])
    # Return edit distance, offset into T, edit transcript
    return mn, off, xcript, D

# This module is for your reference to understand the usage
if len(sys.argv) != 3:
    print("Usage: python3 hw1q1b.py <input_file> <output_file>")
    sys.exit(1)

# Assign the input and output filenames from command-line arguments
input_file = sys.argv[1] # First argument: input filename
output_file = sys.argv[2] # Second argument: output filename

# Open both input and output files - input file for reading and output file for writing
with open(input_file, 'r') as in_file, open(output_file, 'w') as out_file:

    line_1 = in_file.readline().strip()
    line_2 = in_file.readline().strip()

    if len(line_1) == 0 or len(line_2) == 0:
        out_file.write("0")
        sys.exit(0)

    mn, off, xcript, D = kEditDp(line_1, line_2)

    out_file.write(str(mn))
