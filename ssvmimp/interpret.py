from __future__ import absolute_import, division, print_function
from collections import OrderedDict


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


def get_filter_imp_mats(filters, scores, max_mismatches):
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

    for filter1, filter1_gap_vector in zip(filters, filter_gap_vectors):
        filter1_imp_mat = np.zeros_like(filter1)
        num_nongap_positions = np.sum(filter1_gap_vector)
        for (filter2, filter2_gap_vector, filter2_score)\
            in zip(filters, filter_gap_vectors, scores):
            #only compare to other filters where the gaps are in the same spot
            if (all(filter1_gap_vector==filter2_gap_vector)):
                match_spots = np.max(filter1==filter2,axis=1)
                #if the number of mismatches is <= target number, the
                #two filters are compatible
                num_matches = np.sum(match_spots)
                num_mismatches = num_nongap_positions - num_matches
                if (num_mismatches <= max_mismatches):
                    per_pos_imp = filter2_score/num_matches
                    filter1_imp_mat +=\
                        (filter1*match_spots[:,None])*per_pos_imp
        filter_imp_mats.append(filter1_imp_mat) 

    filter_imp_mats = np.array(filter_imp_mats)

    return filter_imp_mats
