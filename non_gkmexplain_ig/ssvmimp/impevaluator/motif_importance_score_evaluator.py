import numpy as np
import impevalutils

class MotifImportanceScoreEvaluator(object):
	"""
	Evaluates importance scores assigned by an importance scoring algorithm using:
	seq2motiflist - An ordered dictionary of actual motif placements. Key is sequence name
			value is a list of dictionaries, each dictionary must contain at least 3
			keys - begin (0-indexed inclusive begin index of motif), end (0-indexed
			exclusive end index of motif), motif (the motif name). 
			seq2motiflist must have at least all the keys named in testseq
	testseq - A numpy array of sequence names to be evaluated (must be the same name as what is
		used in seq2motiflist
	impscores - A numpy array of position wise genomic importance scores for the sequences.
		Must be of shape (testseq length, sequence length, 4)
	"""
	def __init__(self, seq2motiflist, testseqs, impscores):
		self.seq2motiflist = seq2motiflist
		self.testseqs = testseqs
		self.seqlength = impscores.shape[1]
		self.impscores = impscores
		self.motif2sequences = impevalutils.get_motif_to_sequences(self.seq2motiflist, testseqs)
		self.windowscores = dict()

	def get_known_motifs(self):
		return self.motif2sequences.keys()

	def get_motif_size(self, motif):
		matches = self.motif2sequences[motif]
		oneseq = matches[matches.keys()[0]][0]
		return (oneseq["end"] - oneseq["begin"]) 

	def get_window_scores(self, motif_size):
		windowscorelen = self.seqlength-motif_size+1
		if str(motif_size) not in self.windowscores:
			evalscores = list()
			for i in range(0,len(self.testseqs)):
				oneseqscores = np.array([np.sum(self.impscores[i][j:j+motif_size]) for j in range(0,windowscorelen)])
				evalscores.append(oneseqscores)
			self.windowscores[str(motif_size)] = np.array(evalscores)
		return self.windowscores[str(motif_size)]
	
	def get_motif_scores(self, motif):
		"""
		Gets two one dimensional arrays (motif_scores, motif_score_labels):
		1) motif_scores - contains scores of motif sized windows of importance scores sliding with stride 1 from one
			end of each sequence to the other. Windows which overlap any motif are omitted, except for windows that
			exactly fit each occurrence of the specified motif. Windows which do not include or overlap any motif 
			are included.
		2) motif_score_labels -  exactly same size as motif_scores. Contains the corresponding labels of the above scores, 
			-1 for windows that do not include or overlap any motif, +1 for windows that exactly fit the specified 
			motif
		"""
		motif_size = self.get_motif_size(motif)
		window_scores = self.get_window_scores(motif_size)
		motif_scores = list()
		motif_score_labels = list()
		for i in range(0, len(self.testseqs)):
			seq = self.testseqs[i]
			motiflist = self.seq2motiflist[seq]
			marked = np.full((window_scores[i].shape[0]), -1) #Initially mark all windows negative
			if motiflist is not None:
				remember = list()
				for motifdetails in motiflist:
					begin = motifdetails["begin"]
					end = motifdetails["end"]
					listmotif = motifdetails["motif"]
					listmotifsize = end - begin
					if listmotif == motif:
						# print("In " + seq + " found motif " + motif + " at " + str(begin) + ":" + str(end))
						remember.append(begin)	#target motif found in this window
					minimum = begin - motif_size + 1
					minimum = (minimum if minimum >= 0 else 0)
					maximum = end
					maximum = (maximum if maximum <= len(window_scores[0]) 
							else len(window_scores[0]))
					marked[minimum:maximum] = 0  # Mark motif overlapping windows for removal
				marked[remember] = 1 # mark all remembered motif matches as 1
			indices2keep = np.nonzero(marked != 0)[0]
			motif_scores = motif_scores + np.ndarray.tolist(window_scores[i][indices2keep])
			motif_score_labels = motif_score_labels + np.ndarray.tolist(marked[indices2keep])
		final_motif_scores = np.array(motif_scores)
		final_motif_score_labels = np.array(motif_score_labels)
		return (final_motif_scores, final_motif_score_labels)
		
		
		
