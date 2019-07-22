This code is designed to be run in the folder `gm12878_sequence_sets`

Models were trained by running the following commands; note that `-t 3` specifies the gkmrbf kernel, while `-t 2` is the standard gkm kernel. The help prompt for `gkmtrain` states that "RBF kernels (3, 5 and 6) work best with -c 10 -g 2", hence the non-default parameter setting. 

    #negset 1
    ~/lsgkm/bin/gkmtrain -t 3 -l 10 -k 6 -d 3 -c 10 -g 2 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset1

    ~/lsgkm/bin/gkmtrain -t 2 -l 10 -k 6 -d 3 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t2_l10_k6_d3_t16_negset1

    #negset 2
    ~/lsgkm/bin/gkmtrain -t 3 -l 10 -k 6 -d 3 -c 10 -g 2 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.2.1.fa gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset2

    ~/lsgkm/bin/gkmtrain -t 2 -l 10 -k 6 -d 3 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.2.1.fa gkmsvm_t2_l10_k6_d3_t16_negset2

    #negset 3
    ~/lsgkm/bin/gkmtrain -t 3 -l 10 -k 6 -d 3 -c 10 -g 2 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.3.1.fa gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset3

    ~/lsgkm/bin/gkmtrain -t 2 -l 10 -k 6 -d 3 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.3.1.fa gkmsvm_t2_l10_k6_d3_t16_negset3

    #negset 4
    ~/lsgkm/bin/gkmtrain -t 3 -l 10 -k 6 -d 3 -c 10 -g 2 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.4.1.fa gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset4

    ~/lsgkm/bin/gkmtrain -t 2 -l 10 -k 6 -d 3 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.4.1.fa gkmsvm_t2_l10_k6_d3_t16_negset4

    #negset 5
    ~/lsgkm/bin/gkmtrain -t 3 -l 10 -k 6 -d 3 -c 10 -g 2 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.5.1.fa gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset5

    ~/lsgkm/bin/gkmtrain -t 2 -l 10 -k 6 -d 3 -T 16 gm12878_shared.fa nullseqs_gm12878_shared.5.1.fa gkmsvm_t2_l10_k6_d3_t16_negset5

To ascertain that the gkmrbf was performing better than the gkm kernel, cross validation runs were performed using the commands:

    ~/lsgkm/bin/gkmtrain -t 3 -l 10 -k 6 -d 3 -c 10 -g 2 -T 16 -x 5 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t3_l10_k6_d3_c10_g2_t16_x5

    ~/lsgkm/bin/gkmtrain -t 2 -l 10 -k 6 -d 3 -T 16 -x 5 gm12878_shared.fa nullseqs_gm12878_shared.1.1.fa gkmsvm_t2_l10_k6_d3_t16_x5

This generated the files `gkmsvm_t2_l10_k6_d3_t16_x5.cvpred.txt` and `gkmsvm_t3_l10_k6_d3_c10_g2_t16_x5.cvpred.txt`. The auroc was computed using the following commands:

    python compute_auroc.py gkmsvm_t2_l10_k6_d3_t16_x5.cvpred.txt 
    python compute_auroc.py gkmsvm_t3_l10_k6_d3_c10_g2_t16_x5.cvpred.txt

This yields 0.9390508834427328 and 0.9432129964790918 respectively, confirming the advantage of the gkmrbf kernel.

To perform the dsQTL analysis, follow [this README](https://github.com/kundajelab/gkmexplain/tree/master/dsQTL/gm12878_sequence_sets/dsqtl_analysis)
