module load perl
module load homer

cat positives_train.fa positives_test.fa > all_positives.fa
cat negatives_train.fa negatives_test.fa > all_negatives.fa
findMotifs.pl all_positives.fa fasta motifResults/ -fasta all_negatives.fa
