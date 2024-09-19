import numpy as np

# functions for handling FASTQ, provided in https://nbviewer.org/github/BenLangmead/comp-genomics-class/blob/master/notebooks/FASTQ.ipynb
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

# function for handling FASTA, mostly provided in https://nbviewer.org/github/BenLangmead/comp-genomics-class/blob/master/notebooks/FASTA.ipynb
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
            # append nucleotides to current sequence, ignoring any non-nucleotide characters
            string_list = []
            source_string = ln.rstrip()
            for c in source_string:
                if c in 'ACGT':
                    string_list.append(c)
            fa[current_short_name].append(''.join(string_list))
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
fasta_filename = sys.argv[1] # First argument: fasta input filename
fastq_filename = sys.argv[2] # Second argument: fastq input filename
output_file = sys.argv[3] # Third argument: output filename

# Open both input and output files - input file for reading and output file for writing
with open(fasta_filename, 'r') as fasta_file, open(fastq_filename, 'r') as fastq_file, open(output_file, 'w') as out_file:

    # parse fasta using the general fasta parser, and then get only the first genome
    fasta_dict = parse_fasta(fasta_file)
    for key in fasta_dict:
        reference_sequence = fasta_dict[key]
        break

    # parse fastq
    reads = parse_fastq(fastq_file)

    # make a corresponding k-mer index out of the reference genome
    kmer_index = make_kmer_index(reference_sequence, k=6)

    best_hits_kmer = []
    best_hits_number = -1

    already_checked_reads = {''}

    first_read = True

    for read in reads:
        # ignore all non-sequence data
        _, sequence, _ = read

        # ignore duplicate reads (apparently necessary)
        if sequence in already_checked_reads:
            continue
        already_checked_reads.add(sequence)

        # track the indices we have already attempted to align this read at
        indices_already_checked = set()

        # we assume reads have length of exactly 30 - split it into 5 groups of 6
        num_index_hits = []
        index_by_num_mismatches = {}

        # we have 5 partitions of 6 letters each
        for i in range(5):
            sub_seq = sequence[6*i:6*i+6]

            if sub_seq not in kmer_index:
                continue

            # get all places where this partition exactly matches
            indices = kmer_index[sub_seq]

            num_index_hits.append(str(len(indices)))

            # each matching index is the possibility of an approximate match
            for index in indices:

                # since we matched the i-th partition, to check the whole string we have to shift our index back
                shifted_index = index - i*6

                # if we have already checked this index for this read, there is no point in doing so again
                if shifted_index in indices_already_checked:
                    continue
                indices_already_checked.add(shifted_index)

                # ignore substrings that go off the ends of the reference genome
                if shifted_index < 0 or shifted_index + 30 > len(reference_sequence):
                    continue

                reference_substring = reference_sequence[shifted_index:shifted_index+30]
                num_differences = 0

                for c1, c2 in zip(reference_substring, sequence):
                    # character-by-character check for differences
                    if c1 != c2:
                        num_differences += 1
                    if num_differences > 4:
                        break

                if num_differences not in index_by_num_mismatches:
                    # we initialize this as a set because duplicate matching indices are not useful to us
                    index_by_num_mismatches[num_differences] = set()

                # add this to the our map of mismatches count to indices
                index_by_num_mismatches[num_differences].add(shifted_index)
                
        if first_read:
            first_read = False
        else:
            out_file.write('\n')


        out_file.write(' '.join(num_index_hits))
        for i in range(5):

            out_file.write(' ' + str(i) + ':')

            if i not in index_by_num_mismatches:
                continue

            indices = list(index_by_num_mismatches[i])
            indices.sort()
            
            first = True
            for index in indices:
                out_file.write(str(index))
                if first:
                    first = False
                else:
                    out_file.write(',')

    