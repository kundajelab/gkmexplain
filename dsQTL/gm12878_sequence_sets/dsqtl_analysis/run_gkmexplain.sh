#!/usr/bin/env bash 

run_gkmexplain_func () {
    prefix=$1 
    flanksize=$2
    #For the positive set...

    #Run gkmexplain, which will generate scores for all three possible mutations
    ~/lsgkm/bin/gkmexplain -m 5 "posmajor_"$flanksize"flank_coords.fa" $prefix.model.txt gkmexplain_out/"positives_allbases_"$flanksize"_"$prefix.txt

    #Extract the score corresponding to the base that is in the minor allele file
    #Recall that dsqtl_test_pos.minor.fa contains a 9bp flank around the allele;
    # thus, substr($_,9,1) extracts the character corresponding to the allele
    #As a sanity check, this code will also print out the allele it identifies
    # as the minor allele in the output file, which is
    #gkmexplain_out/positives_$flanksize_$modelprefix.txt. You should inspect
    # this for a few examples to see if it's correct.
    paste gkmexplain_out/"positives_allbases_"$flanksize"_"$prefix.txt <(perl -lane 'if ($.%2==0) {print substr($_,9,1)}' dsqtl_test_pos.minor.fa) | perl -lane 'if ($F[3] eq "A") {$base=0;} if ($F[3] eq "C") {$base=1} if ($F[3] eq "G") {$base=2} if ($F[3] eq "T") {$base=3} @_ = split(/,/,$F[2]); print $F[0]."\t".$_[$base]."\t".$base."\t".$F[3]' > gkmexplain_out/"positives_"$flanksize"_"$prefix.txt

    #Repeat for negative set
    ~/lsgkm/bin/gkmexplain -m 5 "negmajor_"$flanksize"flank_coords.fa" $prefix.model.txt gkmexplain_out/"negatives_allbases_"$flanksize"_"$prefix.txt
    paste gkmexplain_out/"negatives_allbases_"$flanksize"_"$prefix.txt <(perl -lane 'if ($.%2==0) {print substr($_,9,1)}' dsqtl_test_neg.minor.fa) | perl -lane 'if ($F[3] eq "A") {$base=0;} if ($F[3] eq "C") {$base=1} if ($F[3] eq "G") {$base=2} if ($F[3] eq "T") {$base=3} @_ = split(/,/,$F[2]); print $F[0]."\t".$_[$base]."\t".$base."\t".$F[3]' > gkmexplain_out/"negatives_"$flanksize"_"$prefix.txt
}

run_gkmexplain_func gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset1 51
run_gkmexplain_func gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset2 51
run_gkmexplain_func gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset3 51
run_gkmexplain_func gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset4 51
run_gkmexplain_func gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset5 51
