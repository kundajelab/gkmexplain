import numpy as np
import re


def load_motif_matches(motif_match_file, doprint=False):
	"""
	Loads a homer motif match file into an ordered dictionary with key as sequence name
	and value as list of dictionaries each containing the keys - motif, sequence, 
	begin (0-indexed inclusive begin index of motif), end (0-indexed exclusive end index), 
	strand (+ or -), seqval. Each dictionary
	represents one motif match on that sequence
	"""
        motif_matches = OrderedDict()
        fp = open(motif_match_file, "r")
	if doprint:
        	print("#Loading " + motif_match_file + " ...")
        numlines = 0
        for line in fp:
                match = re.match("((\w|\-)+)\s+((\w|\:|\-)+)\s+(\d+)\s+(\d+)\s+(\+|\-)\s+.+\s+(\w+)$", line)
                if match:
                        numlines = numlines + 1
                        motif = match.group(1)
                        sequence = match.group(3)
                        begin = int(match.group(5))
                        end = int(match.group(6))
                        strand = match.group(7)
                        seqval = match.group(8)
                        entry = dict()
                        entry['motif'] = motif
                        entry['sequence'] = sequence
			entry['begin'] = begin-1 # Homer motif match file is 1 indexed, convert to 0
                        entry['end'] = end # Homer motif match file is 1 indexed AND inclusive, convert to 0 and exclusive
                        entry['strand'] = strand
                        entry['seqval'] = seqval
                        if sequence not in motif_matches:
                                motif_matches[sequence] = list()
                        motif_matches[sequence].append(entry)
        fp.close()
	if doprint:
        	print("#Loaded " + str(numlines) + " motif matches in " + str(len(motif_matches.keys())) + " sequences")
        return motif_matches


def get_motif_to_sequences(motif_matches, sequence_names):
	"""
	For the sequences named in sequence_names, create a dictionary of motif names to dictionaries. Each inner
	dictionary (corresponding to each motif name) is keyed by sequence name, and has as value a list of dictionaries
	each describing where that motif was found in that sequence. These dictionaries contain the following
	keys: begin (0 indexed), end (0 indexed, exclusive) 
	"""
	motif2sequences = dict()
	for sequence in sequence_names:
		motiflist = motif_matches[sequence]
		for motifdetails in motiflist:
			motif = motifdetails["motif"]
			if motif not in motif2sequences:
				motif2sequences[motif] = dict()
			seqdict = motif2sequences[motif]
			if sequence not in seqdict:
				seqdict[sequence] = list()
			occurences = seqdict[sequence]
			oneoccurence = dict()
			oneoccurence["begin"] = motifdetails["begin"]
			oneoccurence["end"] = motifdetails["end"]
			occurences.append(oneoccurence)
	return motif2sequences

