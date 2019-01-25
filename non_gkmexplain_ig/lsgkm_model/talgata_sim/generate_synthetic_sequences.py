#!/usr/bin/env python
import simdna
import simdna.synthetic as sn
reload(sn)
from collections import OrderedDict
import numpy as np
import random

#background frequence
background_frequency = OrderedDict([('A', 0.3), ('C', 0.2), ('G', 0.2), ('T', 0.3)])

#read in the motifs file
loaded_motifs = sn.LoadedEncodeMotifs(
                    fileName=simdna.ENCODE_MOTIFS_PATH,
                    pseudocountProb=0.0001)

sequenceSetGenerators = []
for motif_set,name_prefix,num_seqs,mean in [
                   (('GATA_disc1', 'TAL1_known1'),'gata_tal1',60000,1),
                   (('GATA_disc1',), 'gata_only',20000,2),
                   (('TAL1_known1',), 'tal1_only',20000,2),
                   ([], 'empty', 20000, None)]:
    embedInBackground = sn.EmbedInABackground(
        backgroundGenerator=sn.ZeroOrderBackgroundGenerator(seqLength=200),
        embedders=[
            sn.RepeatedEmbedder(
                sn.SubstringEmbedder(
                    sn.ReverseComplementWrapper(
                        substringGenerator=sn.PwmSamplerFromLoadedMotifs(
                            loadedMotifs=loaded_motifs,
                            motifName=motif_name)
                    ),
                    positionGenerator=sn.UniformPositionGenerator(),
                    name=motif_name),
                quantityGenerator=sn.MinMaxWrapper(
                    sn.PoissonQuantityGenerator(mean),
                    theMax=3, theMin=1),
            )
            for motif_name in motif_set
        ],
       namePrefix=name_prefix+"_")
    sequenceSetGenerators.append(
        sn.GenerateSequenceNTimes(embedInBackground, N=num_seqs))

label_names = ["task1", "task2", "task3"]
#map motifs to the set of tasks they are relevant for
motifs_to_tasks = {("GATA_disc1",):[1],
                   ("TAL1_known1",):[2],
                   ("GATA_disc1", "TAL1_known1"):[0]}

def labeling_function(label_generator, generated_sequence):
    labels = [0,0,0]
    for motif_set, tasks in motifs_to_tasks.items():
        if (all([generated_sequence.additionalInfo.isInTrace(motif)
             for motif in motif_set])):
            for task in tasks:
                labels[task] = 1
    return labels

np.random.seed(1234)
random.seed(1234)
sequenceSet = sn.ChainSequenceSetGenerators(*sequenceSetGenerators)

sn.printSequences("sequences.simdata", sequenceSet,       
                         includeFasta=True, includeEmbeddings=True,
                         shuffle=False,
                         labelGenerator=sn.LabelGenerator(
                            labelNames=label_names,
                            labelsFromGeneratedSequenceFunction=labeling_function))

