# Import the sys module to access command-line arguments
import sys

# the below is taken from the FASTQ course notebook
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

def suffix_prefix_match(str1, str2, min_overlap):
    if len(str2) < min_overlap:
        return 0
    str2_prefix = str2[:min_overlap]
    str1_pos = -1
    while True:
        str1_pos = str1.find(str2_prefix, str1_pos + 1)
        if str1_pos == -1:
            return 0
        str1_suffix = str1[str1_pos:]
        if str2.startswith(str1_suffix):
            return len(str1_suffix)


def reads_to_dict(reads):
    read_dict = dict()
    for read in reads:
        read_dict[read[0]] = read[1]

    return read_dict

def make_kmer_table(seqs, k):
    """ Given read dictionary and integer k, return a dictionary that
    maps each k-mer to the set of names of reads containing the k-mer. """
    table = {}
    for name, seq in seqs.items():
        for i in range(0, len(seq) - k + 1):
            kmer = seq[i:i+k]
            if kmer not in table:
                table[kmer] = set()
            table[kmer].add(name)
    return table

# This module is for your reference to understand the usage
if len(sys.argv) != 4:
    print("Usage: python3 hw1q1b.py <input_file> <integer_k> <output_file>")
    sys.exit(1)

# Assign the input and output filenames from command-line arguments
fastq_file = sys.argv[1] # First argument: input FASTQ filename
integer_in = sys.argv[2] # Second argument: integer K, corresponding to min suffix/prefix match length
output_file = sys.argv[3] # Second argument: output filename

try:
    K = int(integer_in)
except ValueError:
    print("Second argument must be of integer type")
    sys.exit(1)

first = True

best_match_for_read = {}
best_len_for_read = {}

# Open both input and output files - input file for reading and output file for writing
with open(fastq_file, 'r') as in_file:

    # create dict of reads from FASTQ, then make kmer table
    reads = reads_to_dict(parse_fastq(in_file))
    kmer_table = make_kmer_table(reads, K)

    previously_compared = set()

    for key, relevant_reads in kmer_table.items():

        # each read here shares this Kmer with all others here
        for read_A in relevant_reads:

            if read_A not in best_match_for_read:
                best_match_for_read[read_A] = None
                best_len_for_read[read_A] = 0

            for read_B in relevant_reads:
                # skip self, also skip if we have compared these two before
                if read_A == read_B or (read_A, read_B) in previously_compared:
                    continue
                
                # compute match len
                new_match_len = suffix_prefix_match(reads[read_A], reads[read_B], K)

                if new_match_len > best_len_for_read[read_A]:
                    # new unique longest prefix match
                    best_len_for_read[read_A] = new_match_len
                    best_match_for_read[read_A] = read_B
                elif new_match_len == best_len_for_read[read_A]:
                    # in this case, they are equal - we nullify the previous stored best match, since it is no longer unique
                    best_match_for_read[read_A] = None

                previously_compared.add((read_A, read_B))
                
with open(output_file, 'w') as out_file:
    for read in best_match_for_read:

        if best_match_for_read[read] is not None:

            if first:
                first = False
            else:
                out_file.write('\n')

            out_file.write(read)
            out_file.write(" " + str(best_len_for_read[read]) + " ")
            out_file.write(best_match_for_read[read])



            



            
