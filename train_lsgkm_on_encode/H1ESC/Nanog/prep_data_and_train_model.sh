#!/usr/bin/env bash
wget https://www.encodeproject.org/files/ENCFF148PBJ/@@download/ENCFF148PBJ.bed.gz -O conservative_peaks.bed.gz
wget https://www.encodeproject.org/files/ENCFF379EPK/@@download/ENCFF379EPK.bed.gz -O optimal_peaks.bed.gz

ln -s /mnt/data/integrative/dnase/ENCSR000EMU_ENCSR794OFW.H1_Cells.UW_Stam.DNase-seq/out_50m/peak/idr/pseudo_reps/rep1/ENCSR000EMU_ENCSR794OFW.H1_Cells.UW_Stam.DNase-seq_rep1-pr.IDR0.1.narrowPeak.gz bg_dnase.bed.gz

zcat optimal_peaks.bed.gz | perl -lane 'print($F[0]."\t".($F[1]+$F[9]-100)."\t".($F[1]+$F[9]+100))' | gzip -c > positive_set_full.bed.gz
#negative set is 200bp around summit of accessible peaks that don't overlap 1kb within any optimal or conservative peak
zcat conservative_peaks.bed.gz optimal_peaks.bed.gz | perl -lane 'print($F[0]."\t".($F[1]+$F[9]-500)."\t".($F[1]+$F[9]+500))' | gzip -c > 1kb_around_optimal_or_conservative_peaks.bed.gz
zcat bg_dnase.bed.gz | perl -lane 'print($F[0]."\t".($F[1]+$F[9]-100)."\t".($F[1]+$F[9]+100))' | gzip -c > prefiltered_neg_set.bed.gz
bedtools intersect -a prefiltered_neg_set.bed.gz -b 1kb_around_optimal_or_conservative_peaks.bed.gz -v -wa | gzip -c > neg_set_full.bed.gz

#subsample the negative set
# class imbalance is roughly 1:3 in favour of negatives
zcat neg_set_full.bed.gz | perl -lane 'if ($.%5==1) {print $_}' | gzip -c > subsampled_neg_set.bed.gz

#use chr1 and 2 for the test set
zcat optimal_peaks.bed.gz | egrep -w 'chr1|chr2' | gzip -c > positives_test_set.bed.gz
zcat optimal_peaks.bed.gz | egrep -w -v 'chr1|chr2' | gzip -c > positives_train_set.bed.gz
zcat subsampled_neg_set.bed.gz | egrep -w 'chr1|chr2' | gzip -c > negatives_test_set.bed.gz
zcat subsampled_neg_set.bed.gz | egrep -w -v 'chr1|chr2' | gzip -c > negatives_train_set.bed.gz


bedtools getfasta -fi hg19.genome.fa -bed positives_train_set.bed.gz > positives_train.fa
bedtools getfasta -fi hg19.genome.fa -bed positives_test_set.bed.gz > positives_test.fa
bedtools getfasta -fi hg19.genome.fa -bed negatives_train_set.bed.gz > negatives_train.fa
bedtools getfasta -fi hg19.genome.fa -bed negatives_test_set.bed.gz > negatives_test.fa

~/lsgkm/src/gkmtrain -T 16 -w 2.88 positives_train.fa negatives_train.fa lsgkm_defaultsettings_w2p88_
