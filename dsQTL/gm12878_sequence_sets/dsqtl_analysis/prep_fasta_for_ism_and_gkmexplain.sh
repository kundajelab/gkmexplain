#!/usr/bin/env bash

prep_fasta_func () {
    halfflank=$1
    halfflankplusone=`expr $halfflank + 1`
    fullwidth=`expr $halfflank + $halfflankplusone`

    perl -lane 'if ($.%2==1) {@_ = split(/[>:\-]/,$_); print ($_[1]."\t".($_[2]+9-'$halfflankplusone')."\t".($_[2]+9+'$halfflank'))}' dsqtl_test_pos.major.fa > "posregion_"$fullwidth"flank_coords.bed"
    bedtools getfasta -fi hg18.fa -bed "posregion_"$fullwidth"flank_coords.bed" > "posregion_"$fullwidth"flank_coords.fa"
    paste "posregion_"$fullwidth"flank_coords.fa" dsqtl_test_pos.major.fa | perl -lane 'if ($.%2==1) {print $F[0];} else {$start = substr($F[0],0,'$halfflank'); $end = substr($F[0],'$halfflankplusone'); $mid = substr($F[1],9,1); print(uc($start.$mid.$end))}' > "posmajor_"$fullwidth"flank_coords.fa"
    paste "posregion_"$fullwidth"flank_coords.fa" dsqtl_test_pos.minor.fa | perl -lane 'if ($.%2==1) {print $F[0];} else {$start = substr($F[0],0,'$halfflank'); $end = substr($F[0],'$halfflankplusone'); $mid = substr($F[1],9,1); print(uc($start.$mid.$end))}' > "posminor_"$fullwidth"flank_coords.fa"

    perl -lane 'if ($.%2==1) {@_ = split(/[>:\-]/,$_); print ($_[1]."\t".($_[2]+9-'$halfflankplusone')."\t".($_[2]+9+'$halfflank'))}' dsqtl_test_neg.major.fa > "negregion_"$fullwidth"flank_coords.bed"
    bedtools getfasta -fi hg18.fa -bed "negregion_"$fullwidth"flank_coords.bed" > "negregion_"$fullwidth"flank_coords.fa"
    paste "negregion_"$fullwidth"flank_coords.fa" dsqtl_test_neg.major.fa | perl -lane 'if ($.%2==1) {print $F[0];} else {$start = substr($F[0],0,'$halfflank'); $end = substr($F[0],'$halfflankplusone'); $mid = substr($F[1],9,1); print(uc($start.$mid.$end))}' > "negmajor_"$fullwidth"flank_coords.fa"
    paste "negregion_"$fullwidth"flank_coords.fa" dsqtl_test_neg.minor.fa | perl -lane 'if ($.%2==1) {print $F[0];} else {$start = substr($F[0],0,'$halfflank'); $end = substr($F[0],'$halfflankplusone'); $mid = substr($F[1],9,1); print(uc($start.$mid.$end))}' > "negminor_"$fullwidth"flank_coords.fa"

}

prep_fasta_func 9
prep_fasta_func 15
