#!/usr/bin/env bash 

run_ism_func () {
    prefix=$1 
    flanksize=$2
    ~/lsgkm/bin/gkmpredict -T 16 "pos_"$flanksize"flank_coords.fa" $prefix.model.txt ism_out/"pos_major_"$flanksize"_"$prefix.txt
    ~/lsgkm/bin/gkmpredict -T 16 "posminor_"$flanksize"flank_coords.fa" $prefix.model.txt ism_out/"pos_minor_"$flanksize"_"$prefix.txt
    paste ism_out/"pos_major_"$flanksize"_"$prefix.txt ism_out/"pos_minor_"$flanksize"_"$prefix.txt | perl -lane 'print $F[0]."\t".($F[3]-$F[1])' > ism_out/"ism_diff_pos_"$flanksize"_"$prefix.txt
    ~/lsgkm/bin/gkmpredict -T 16 "neg_"$flanksize"flank_coords.fa" $prefix.model.txt ism_out/"neg_major_"$flanksize"_"$prefix.txt
    ~/lsgkm/bin/gkmpredict -T 16 "negminor_"$flanksize"flank_coords.fa" $prefix.model.txt ism_out/"neg_minor_"$flanksize"_"$prefix.txt
    paste ism_out/"neg_major_"$flanksize"_"$prefix.txt ism_out/"neg_minor_"$flanksize"_"$prefix.txt | perl -lane 'print $F[0]."\t".($F[3]-$F[1])' > ism_out/"ism_diff_neg_"$flanksize"_"$prefix.txt
}

run_ism_func gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset1 19 
run_ism_func gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset1 101
