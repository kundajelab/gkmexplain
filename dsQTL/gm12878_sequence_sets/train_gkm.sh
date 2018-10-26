#cross validation runs to ascertain that the gkmrbf model was performing better
#~/lsgkm/bin/gkmtrain -t 3 -l 10 -k 6 -d 3 -c 10 -g 2 -T 16 -x 5 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t3_l10_k6_d3_c10_g2_t16_x5

#~/lsgkm/bin/gkmtrain -t 2 -l 10 -k 6 -d 3 -T 16 -x 5 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t2_l10_k6_d3_t16_x5

#negset 1
~/lsgkm/bin/gkmtrain -t 3 -l 10 -k 6 -d 3 -c 10 -g 2 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset1

~/lsgkm/bin/gkmtrain -t 2 -l 10 -k 6 -d 3 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t2_l10_k6_d3_t16_negset1

#negset 2
~/lsgkm/bin/gkmtrain -t 3 -l 10 -k 6 -d 3 -c 10 -g 2 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset2

~/lsgkm/bin/gkmtrain -t 2 -l 10 -k 6 -d 3 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t2_l10_k6_d3_t16_negset2

#negset 3
~/lsgkm/bin/gkmtrain -t 3 -l 10 -k 6 -d 3 -c 10 -g 2 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset3

~/lsgkm/bin/gkmtrain -t 2 -l 10 -k 6 -d 3 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t2_l10_k6_d3_t16_negset3

#negset 4
~/lsgkm/bin/gkmtrain -t 3 -l 10 -k 6 -d 3 -c 10 -g 2 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset4

~/lsgkm/bin/gkmtrain -t 2 -l 10 -k 6 -d 3 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t2_l10_k6_d3_t16_negset4

#negset 5
~/lsgkm/bin/gkmtrain -t 3 -l 10 -k 6 -d 3 -c 10 -g 2 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset5

~/lsgkm/bin/gkmtrain -t 2 -l 10 -k 6 -d 3 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t2_l10_k6_d3_t16_negset5
