#!/usr/bin/env bash

for negset in 1 2 3 4 5; do
	gkmexplainperf=`./compute_perf_stats.py gkmexplain_out/positives_51_gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset$negset.txt gkmexplain_out/negatives_51_gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset$negset.txt`

	ismperf=`./compute_perf_stats.py ism_out/ism_diff_pos_51_gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset$negset.txt ism_out/ism_diff_neg_51_gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset$negset.txt`

	deltasvmgkmrbfperf=`./compute_perf_stats.py deltasvm_out/positives_gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset$negset.txt deltasvm_out/negatives_gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset$negset.txt`

	deltasvmgkmperf=`./compute_perf_stats.py deltasvm_out/positives_gkmsvm_t2_l10_k6_d3_t16_negset$negset.txt deltasvm_out/negatives_gkmsvm_t2_l10_k6_d3_t16_negset$negset.txt`

	echo "NegativeSet $negset GkmExplain:$gkmexplainperf ISM:$ismperf deltasvm-gkmrbf:$deltasvmgkmrbfperf deltasvm-gkm:$deltasvmgkmperf"
done
