#!/usr/bin/env bash 

run_gkmexplain_func () {
    prefix=$1 
    flanksize=$2
    ~/lsgkm/bin/gkmexplain -m 5 "pos_"$flanksize"flank_coords.fa" $prefix.model.txt gkmexplain_out/"positives_allbases_"$flanksize"_"$prefix.txt
    paste gkmexplain_out/"positives_allbases_"$flanksize"_"$prefix.txt <(perl -lane 'if ($.%2==0) {print substr($_,9,1)}' dsqtl_test_pos.minor.fa) | perl -lane 'if ($F[3] eq "A") {$base=0;} if ($F[3] eq "C") {$base=1} if ($F[3] eq "G") {$base=2} if ($F[3] eq "T") {$base=3} @_ = split(/,/,$F[2]); print $F[0]."\t".$_[$base]."\t".$base."\t".$F[3]' > gkmexplain_out/"positives_"$flanksize"_"$prefix.txt

    ~/lsgkm/bin/gkmexplain -m 5 "neg_"$flanksize"flank_coords.fa" $prefix.model.txt gkmexplain_out/"negatives_allbases_"$flanksize"_"$prefix.txt
    paste gkmexplain_out/"negatives_allbases_"$flanksize"_"$prefix.txt <(perl -lane 'if ($.%2==0) {print substr($_,9,1)}' dsqtl_test_neg.minor.fa) | perl -lane 'if ($F[3] eq "A") {$base=0;} if ($F[3] eq "C") {$base=1} if ($F[3] eq "G") {$base=2} if ($F[3] eq "T") {$base=3} @_ = split(/,/,$F[2]); print $F[0]."\t".$_[$base]."\t".$base."\t".$F[3]' > gkmexplain_out/"negatives_"$flanksize"_"$prefix.txt
}

run_gkmexplain_func gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset1 19
run_gkmexplain_func gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset1 101
