
module load meme/4.12.0
cat negatives_train.fa negatives_test.fa > all_negatives.fa
cat positives_train.fa positives_test.fa > all_positives.fa
meme-chip -fimo-skip -spamo-skip -meme-nmotifs 10 -meme-p 20 -neg all_negatives.fa all_positives.fa
