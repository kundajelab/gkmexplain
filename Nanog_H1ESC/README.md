For a colab notebook that preps the data, trains a model, computes
gkmexplain scores and runs TF-MoDISco, see:
[https://github.com/kundajelab/gkmexplain/blob/master/lsgkmexplain_Nanog.ipynb](https://github.com/kundajelab/gkmexplain/blob/master/lsgkmexplain_Nanog.ipynb) or open the link [https://colab.research.google.com/github/kundajelab/gkmexplain/blob/master/lsgkmexplain_Nanog.ipynb](https://colab.research.google.com/github/kundajelab/gkmexplain/blob/master/lsgkmexplain_Nanog.ipynb)

HOMER was run with the following commands:

```
#module load perl
#module load homer
cat positives_train.fa positives_test.fa > all_positives.fa
cat negatives_train.fa negatives_test.fa > all_negatives.fa
findMotifs.pl all_positives.fa fasta motifResults/ -fasta all_negatives.fa
```

`Gandhi et al and HOMER motifs.ipynb` runs the motif discovery method of
Gandhi et al, and also visualizes the significant HOMER motifs.

`meme_results.txt.gz` has the results of running MEME. The job details were:
```
(Primary) Sequences	A set of 5647 DNA sequences, all 200 in length, from the file all_positives.fa.
Control Sequences	A set of 5981 DNA sequences, all 200 in length, from the file all_negatives.fa.
Background	A order-0 background generated from the supplied sequences.
Discovery Mode	Discriminative: creates a discriminative position-specific prior (PSP) and applies Classic mode
Site Distribution	Zero or one occurrence (of a contributing motif site) per sequence.
Motif Count	Searching for 10 motifs.
Motif Width	Between 6 wide and 50 wide (inclusive).
```
