from __future__ import absolute_import, division, print_function
from collections import OrderedDict
import numpy as np
import sys


def get_filter_matches(kmer_string, filter_strings, max_mismatches):
    """Get string representing the filters that match a particular kmer.

    Arguments: 
        kmer_string: a string representing the kmer, gapped or ungapped.\
            Example: GATAAG or G TA G

        filter_strings: an iterable of strings representing the filters

        max_mismatches: int, number of mismatches allowed before considering
            a filter a 'match to the kmer
    """
    matching_filters = []
    for filter_string in filter_strings:
        match = True
        mismatches_so_far = 0
        for kmer_letter, filter_letter in zip(kmer_string, filter_string):
            if (filter_letter!=" " and kmer_letter!=filter_letter):
                mismatches_so_far += 1
                if mismatches_so_far > max_mismatches:
                    match=False
                    break
        if (match):
            matching_filters.append(filter_string)
    return matching_filters


def get_total_kmer_score(kmer_string, filter_to_score, max_mismatches):
    """Get the total score associated with a kmer.

    Arguments:
        kmer_string: a string representing the kmer, gapped or ungapped.\
            Example: GATAAG or G TA G

        filter_to_score: OrderedDict where key is a string representing\
            the filter (may have gaps) and the value is the score of\
            the filter.

        max_mismatches: int, number of mismatches allowed before considering
            a filter a 'match' to the kmer
    """
    assert isinstance(filter_to_score, OrderedDict)
    filter_matches = get_filter_matches(
        kmer_string=kmer_string,
        filter_strings=filter_to_score.keys(),
        max_mismatches=max_mismatches)
    total_score = 0
    for a_filter in filter_matches:
        total_score += filter_to_score[a_filter]
    return total_score


def get_filter_imp_mats(filters, scores, max_mismatches,
                        progress_update=500):
    """Get filters that can be used to assign importance to individual bases
    """
    assert len(filters.shape)==3
    assert len(filters)==len(scores)
    #filter_gap_vectors are vectors representing where the gaps are
    filter_gap_vectors = np.sum(filters, axis=2)

    filter_imp_mats = []

    #For each filter (denoted filter1), we ask the question:
    # "if the underlying sequence is an exact match to filter1,
    # then which other filters that have
    # gaps in the same locations will also be matched if allowing
    # for max_mismatches?". We can then think of filter1
    # as "acquiring" the importance of all those other filters. For each
    # filter that filter1 is a match to, the total importance of
    # the filter is divided by the number of positions in filter1
    # that matched up and is assigned evenly to those positions

    for filter_idx, (filter1, filter1_gap_vector) in\
        enumerate(zip(filters, filter_gap_vectors)):
        if (filter_idx%progress_update == 0):
            print("On filter index:",filter_idx)
            sys.stdout.flush()

        filter1_imp_mat = np.zeros_like(filter1)
        num_nongap_positions = np.sum(filter1_gap_vector)
        for (filter2, filter2_gap_vector, filter2_score)\
            in zip(filters, filter_gap_vectors, scores):
            #only compare to other filters where the gaps are in the same spot
            if (all(filter1_gap_vector==filter2_gap_vector)):
                match_spots = np.max((filter1==filter2)*filter1,axis=1)
                #if the number of mismatches is <= target number, the
                #two filters are compatible
                num_matches = np.sum(match_spots)
                num_mismatches = num_nongap_positions - num_matches
                if (num_mismatches <= max_mismatches):
                    per_pos_imp = filter2_score/num_matches
                    to_add = (filter1*match_spots[:,None])*per_pos_imp
                    filter1_imp_mat += to_add
                    
        filter_imp_mats.append(filter1_imp_mat) 

    filter_imp_mats = np.array(filter_imp_mats)

    return filter_imp_mats


def get_per_base_filter_contrib_nomismatch(filters):
    """Get filters that can be used to assign importance to individual bases
    Assumes total filter importance is 1. Does not tolerate mismatches
    """
    assert len(filters.shape)==3
    #filter_gap_vectors are vectors representing where the gaps are
    filter_gap_vectors = np.sum(filters, axis=2)

    filter_imp_mats = []

    #For each filter (denoted filter1), we ask the question:
    # "if the underlying sequence is an exact match to filter1,
    # then which other filters that have
    # gaps in the same locations will also be matched if allowing
    # for max_mismatches?". We can then think of filter1
    # as "acquiring" the importance of all those other filters. For each
    # filter that filter1 is a match to, the total importance of
    # the filter is divided by the number of positions in filter1
    # that matched up and is assigned evenly to those positions

    for filter_idx, (filter1, filter1_gap_vector) in\
        enumerate(zip(filters, filter_gap_vectors)):
        filter1_imp_mat = filter1/np.sum(filter1)
        num_nongap_positions = np.sum(filter1_gap_vector)
        filter_imp_mats.append(filter1_imp_mat) 

    filter_imp_mats = np.array(filter_imp_mats)

    return filter_imp_mats


def get_filter_mutation_effects(filters, filter_imp_mats):
    """
    For each filter and corresponding filter importance matrix,\
        get a filter that represents the relative impact of making\
        single mutations at particular positions

    Arguments:
        filter_contribs: the total importance contributed by an exact match\
            to the filter, including mismatches 
    """
    assert len(filters.shape)==3
    assert filters.shape==filter_imp_mats.shape
    assert np.max(np.sum(np.abs(filters),axis=-1))==1 #no col has over one 1
    assert np.min(filters)==0 #min value is 0

    filter_contribs = np.sum(filter_imp_mats, axis=(1,2))

    #for each filter, find an id by treating the ones as digits in a number
    #in base (filters.shape[-1]+1)
    place_values = np.array([(filters.shape[2]+1)**i for
                             i in range(filters.shape[1])])
    filter_digit_vecs = (np.argmax(filters,axis=-1)+1)*np.max(filters,axis=-1)
    filter_id_to_contrib = dict([
        (np.sum(place_values*filter_digit_vec), filter_contrib)
        for (a_filter, filter_digit_vec, filter_contrib)
        in zip(filters, filter_digit_vecs, filter_contribs)])

    filter_mutation_effect_mats = []
    for a_filter, filter_digit_vec, filter_imp_mat, filter_contrib in\
        zip(filters, filter_digit_vecs, filter_imp_mats, filter_contribs):

        filter_mutation_effect_mat = np.array(filter_imp_mat)
        assert len(filter_mutation_effect_mat.shape) == 2

        #get the nongap positions
        nonzero_positions = np.nonzero(np.max(a_filter, axis=-1))[0]
        #iterate over the nongap positions
        for nonzero_position in nonzero_positions:
            original_letter_idx = int(filter_digit_vec[nonzero_position]-1)
            #iterate over all the possible letters at that position
            for letter_idx in range(a_filter.shape[1]):
                #if the letter under consideration is a proposed mutation
                #(i.e. it's not the letter that's already there)
                if letter_idx != original_letter_idx:
                    new_filter_digit_vec = np.array(filter_digit_vec)
                    new_filter_digit_vec[nonzero_position] = letter_idx+1
                    new_filter_id = np.sum(place_values*new_filter_digit_vec)
                    new_filter_contrib = filter_id_to_contrib[new_filter_id]

                    delta = ((new_filter_contrib-filter_contrib)+
                             (filter_imp_mat[nonzero_position,
                                             original_letter_idx]))
                    filter_mutation_effect_mat[nonzero_position,
                                               letter_idx] = delta 
        filter_mutation_effect_mats.append(filter_mutation_effect_mat)
    return np.array(filter_mutation_effect_mats)

