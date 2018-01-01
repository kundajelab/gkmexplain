from __future__ import print_function, absolute_import, division
import itertools
from . import backend as B
import numpy as np


def get_gapped_kmer_embedding_filters_and_func(
        kmer_len, alphabet, num_gaps, num_mismatches):
    filters, biases, string_reps = prep_filters_and_biases(
                                    kmer_len=kmer_len,
                                    alphabet=alphabet,
                                    num_gaps=num_gaps,
                                    num_mismatches=num_mismatches) 
    func = B.get_gapped_kmer_embedding_func(filters=filters, biases=biases)
    return string_reps, func


#prepare filters and biases for scanning strings with conv filters
def prep_filters_and_biases(kmer_len, alphabet,
                            num_gaps, num_mismatches):
    #given the number of gaps and the kmer length,
    #find all unique combinations of positions
    #in the filter that are nonzero (nonzero = not a gap)
    nonzero_position_combos = list(itertools.combinations(
                        iterable=range(kmer_len),
                        r=(kmer_len-num_gaps)))
    #given the number of nonzero positions, get a list of all the possible
    #letter permutations ("permutations" is not the right work, 'product'
    #is a better word since the same letter can appear in multiple positions
    letter_permutations = list(itertools.product(
                            *[list(range(len(alphabet))) for x in
                              range(kmer_len-num_gaps)]))
    filters = []
    biases = []
    #string representations of the filters (positions are comma separated)
    filter_string_reps = [] 

    unique_nonzero_positions = set()
    #for every set of unique nonzero positions
    for nonzero_positions in nonzero_position_combos:
        nonzero_string_representation = [" " for x in range(kmer_len)]
        for nonzero_position in nonzero_positions:
            nonzero_string_representation[nonzero_position] = "X"
        #get a representation which is " " if the position is zero (gapped)
        #and "X" if the position is nonzero
        nonzero_positions_string =\
            ("".join(nonzero_string_representation)).lstrip().rstrip()
        #after stripping trailing and leading gaps, make sure it's not
        #a combo of nonzero positions we have already created filters for
        if (nonzero_positions_string not in unique_nonzero_positions):
            unique_nonzero_positions.add(nonzero_positions_string) 

            #if it's a combo we haven't seen, iterate over the letter
            #permutations and create filters by placing the letters
            #at the nonzero positions
            for letter_permutation in letter_permutations:
                assert len(nonzero_positions)==len(letter_permutation)

                filter_string_rep = [" " for x in range(kmer_len)]
                the_filter = np.zeros((kmer_len, len(alphabet))) 
                for nonzero_position, letter\
                    in zip(nonzero_positions, letter_permutation):
                    the_filter[nonzero_position, letter] = 1 
                    filter_string_rep[nonzero_position] = alphabet[letter]
                filters.append(the_filter)
                biases.append(-(len(nonzero_positions)-1-num_mismatches))
                filter_string_reps.append("".join(filter_string_rep))
    return np.array(filters), np.array(biases), filter_string_reps 
    
