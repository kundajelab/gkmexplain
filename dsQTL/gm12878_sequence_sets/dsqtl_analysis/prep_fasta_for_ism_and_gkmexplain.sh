#!/usr/bin/env bash

perl -lane 'if ($.%2==1) {@_ = split(/[>:\-]/,$_); print ($_[1]."\t".($_[2]+9-151)."\t".($_[2]+9+150))}' dsqtl_test_pos.major.fa > pos_301flank_coords.bed
bedtools getfasta -fi hg18.fa -bed pos_301flank_coords.bed > pos_301flank_coords.fa
paste pos_301flank_coords.fa dsqtl_test_pos.minor.fa | perl -lane 'if ($.%2==1) {print $F[0];} else {$start = substr($F[0],0,150); $end = substr($F[0],151); $mid = substr($F[1],9,1); print($start.$mid.$end)}' > posminor_301flank_coords.fa

perl -lane 'if ($.%2==1) {@_ = split(/[>:\-]/,$_); print ($_[1]."\t".($_[2]+9-151)."\t".($_[2]+9+150))}' dsqtl_test_neg.major.fa > neg_301flank_coords.bed
bedtools getfasta -fi hg18.fa -bed neg_301flank_coords.bed > neg_301flank_coords.fa
paste neg_301flank_coords.fa dsqtl_test_neg.minor.fa | perl -lane 'if ($.%2==1) {print $F[0];} else {$start = substr($F[0],0,150); $end = substr($F[0],151); $mid = substr($F[1],9,1); print($start.$mid.$end)}' > negminor_301flank_coords.fa


perl -lane 'if ($.%2==1) {@_ = split(/[>:\-]/,$_); print ($_[1]."\t".($_[2]+9-51)."\t".($_[2]+9+50))}' dsqtl_test_pos.major.fa > pos_101flank_coords.bed
bedtools getfasta -fi hg18.fa -bed pos_101flank_coords.bed > pos_101flank_coords.fa
paste pos_101flank_coords.fa dsqtl_test_pos.minor.fa | perl -lane 'if ($.%2==1) {print $F[0];} else {$start = substr($F[0],0,50); $end = substr($F[0],51); $mid = substr($F[1],9,1); print($start.$mid.$end)}' > posminor_101flank_coords.fa

perl -lane 'if ($.%2==1) {@_ = split(/[>:\-]/,$_); print ($_[1]."\t".($_[2]+9-51)."\t".($_[2]+9+50))}' dsqtl_test_neg.major.fa > neg_101flank_coords.bed
bedtools getfasta -fi hg18.fa -bed neg_101flank_coords.bed > neg_101flank_coords.fa
paste neg_101flank_coords.fa dsqtl_test_neg.minor.fa | perl -lane 'if ($.%2==1) {print $F[0];} else {$start = substr($F[0],0,50); $end = substr($F[0],101); $mid = substr($F[1],9,1); print($start.$mid.$end)}' > negminor_101flank_coords.fa
