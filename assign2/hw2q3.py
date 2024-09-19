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

    for key in kmer_index:
        # check number of times each key shows up in the reference
        hits = len(kmer_index[key])

        # check if this has beaten out the previously most occuring key
        if hits > best_hits_number:
            best_hits_number = hits
            best_hits_kmer = []
            best_hits_kmer.append(key)

        # if we have a tie, then we store both as instructed
        elif hits == best_hits_number:
            best_hits_kmer.append(key)

    # ensure in order
    best_hits_kmer.sort()

    match_index_tracker = {}
    total_reads = 0

    current_best = -1
    current_best_index = -1

    already_checked_reads = {''}


    for read in reads:
        # ignore all non-sequence data
        _, sequence, _ = read

        # ignore duplicate reads (apparently necessary)
        if sequence in already_checked_reads:
            continue
        already_checked_reads.add(sequence)

        # check against the index, ignore this read if does not match anywhere
        sequence_6mer = sequence[0:6]
        if sequence_6mer not in kmer_index:
            continue
        
        # check all places where the k-mer matches
        for index in kmer_index[sequence_6mer]:
            if reference_sequence[index:index+len(sequence)] == sequence:
                # this read is an exact match to the reference genome
                total_reads += 1

                if index not in match_index_tracker:
                    match_index_tracker[index] = 0
                match_index_tracker[index] += 1

                if match_index_tracker[index] > current_best or (match_index_tracker[index] == current_best and index < current_best_index):
                    # check if this index is the new maximum matching index (breaking ties by smaller index value)
                    current_best = match_index_tracker[index]
                    current_best_index = index

    out_file.write(','.join(best_hits_kmer) + ' ' + str(total_reads) + ' ' + str(current_best_index))


    