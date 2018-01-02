from __future__ import absolute_import, division, print_function
from collections import OrderedDict


def get_filter_matches(kmer_string, filter_strings, num_mismatches):
    """Get string representing the filters that match a particular kmer.

    Arguments: 
        kmer_string: a string representing the kmer, gapped or ungapped.\
            Example: GATAAG or G TA G

        filter_strings: an iterable of strings representing the filters

        num_mismatches: int, number of mismatches allowed before considering
            a filter a 'match to the kmer
    """
    matching_filters = []
    for filter_string in filter_strings:
        match = True
        mismatches_so_far = 0
        for kmer_letter, filter_letter in zip(kmer_string, filter_string):
            if (filter_letter!=" " and kmer_letter!=filter_letter):
                mismatches_so_far += 1
                if mismatches_so_far > num_mismatches:
                    match=False
                    break
        if (match):
            matching_filters.append(filter_string)
    return matching_filters


def get_total_kmer_score(kmer_string, filter_to_score, num_mismatches):
    """Get the total score associated with a kmer.

    Arguments:
        kmer_string: a string representing the kmer, gapped or ungapped.\
            Example: GATAAG or G TA G

        filter_to_score: OrderedDict where key is a string representing\
            the filter (may have gaps) and the value is the score of\
            the filter.

        num_mismatches: int, number of mismatches allowed before considering
            a filter a 'match' to the kmer
    """
    assert isinstance(filter_to_score, OrderedDict)
    filter_matches = get_filter_matches(
        kmer_string=kmer_string,
        filter_strings=filter_to_score.keys(),
        num_mismatches=num_mismatches)
    total_score = 0
    for a_filter in filter_matches:
        total_score += filter_to_score[a_filter]
    return total_score


