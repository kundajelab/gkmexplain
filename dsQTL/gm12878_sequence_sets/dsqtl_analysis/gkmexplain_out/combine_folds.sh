#!/usr/bin/env bash
paste positives_51_gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset*.txt | cut -f 1,2,6,10,14,18 | perl -lane 'print $F[0]."\t".($F[1]+$F[2]+$F[3]+$F[4]+$F[5])' > combined_positives.txt
paste negatives_51_gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset*.txt | cut -f 1,2,6,10,14,18 | perl -lane 'print $F[0]."\t".($F[1]+$F[2]+$F[3]+$F[4]+$F[5])' > combined_negatives.txt
