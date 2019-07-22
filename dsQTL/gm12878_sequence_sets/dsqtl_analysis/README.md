
The model files are symlinked into this directory from the previous one.
The files `dsqtl_test_neg.major.fa`, `dsqtl_test_pos.major.fa`, `dsqtl_test_neg.major.fa` and `dsqtl_test_pos.major.fa` were downloaded and moved into this directory by `../../get_data.sh`.
`hg18.fa` needs to be present in this directory. It can either be symlinked here or downloaded via:

    wget http://hgdownload.cse.ucsc.edu/goldenPath/hg18/bigZips/hg18.2bit
    wget http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/twoBitToFa -O twoBitToFa
    chmod a+x twoBitToFa
    ./twoBitToFa hg18.2bit hg18.fa

To score the variants with deltasvm, execute `./run_deltasvm.sh`. It will produce the results in the `deltasvm_out` directory.

To score the variants with gkmexplain or in-silico mutagenesis (ISM), we first need to decide how much context around the variant to provide. The reason this was not necessary when runnning delatsvm is that deltasvm only gives consideration to the l-mers that immediately overlap the variant; because the l-mer size is 10, this means deltaSVM only considers 9bp of context on either side of the variant, and that is what is provided in the `dsqtl_test_*.*.fa` files downloaded from the deltaSVM website. The script `./prep_fasta_for_ism_and_gkmexplain.sh` pulls in 25bp of context on either side of the variant for use with ISM and GkmExplain. It generates the files `posmajor_51flank_coords.fa`, `posminor_51flank_coords.fa`, `negmajor_51flank_coords.fa` and `negminor_51flank_coords.fa`. The final outputs have been saved in this github repository.

Once the files with the expanded flanks have been prepared, we can run ISM and gkmexplain by calling `run_ism.sh` and `run_gkmexplain.sh`. They will produce results in the `ism_out` and `gkmexplain_out` directories, respectively. The final outputs have been saved in this github repository. 

To reproduce the auPRCs in Figure 8 of the main figure, run `summarize_auprcs.sh`. It gives the output: 

    NegativeSet 1 GkmExplain:0.18905012613037497 ISM:0.1880813240274184 deltasvm-gkmrbf:0.18286977265514853 deltasvm-gkm:0.179178068476846
    NegativeSet 2 GkmExplain:0.1910123884300699 ISM:0.1896758048492444 deltasvm-gkmrbf:0.18648554951967555 deltasvm-gkm:0.18565486895923847
    NegativeSet 3 GkmExplain:0.18522736749748275 ISM:0.18432610308590425 deltasvm-gkmrbf:0.1800054628781844 deltasvm-gkm:0.17697365562496964
    NegativeSet 4 GkmExplain:0.18697771718457107 ISM:0.18569398186553088 deltasvm-gkmrbf:0.18027608051247246 deltasvm-gkm:0.1794275915868459
    NegativeSet 5 GkmExplain:0.19476864677663552 ISM:0.1943242668346119 deltasvm-gkmrbf:0.18733035565708475 deltasvm-gkm:0.1848268442432523


For fun, I also averaged the results over the five folds by running the `combine_folds.sh` script in the `gkmexplain_out`, `ism_out` and `deltasvm_out` directories and compared the performance. This analysis isn't in the paper as I couldn't put any statistical confidence on it. The results are as follows:

    ./compute_perf_stats.py gkmexplain_out/combined_positives.txt gkmexplain_out/combined_negatives.txt
    0.19647080084352467 
    ./compute_perf_stats.py ism_out/combined_positives.txt ism_out/combined_negatives.txt 
    0.1955013882806286
    ./compute_perf_stats.py deltasvm_out/combined_positives_gkmsvm_t3_l10_k6_d3_c10_g2_t16.txt deltasvm_out/combined_negatives_gkmsvm_t3_l10_k6_d3_c10_g2_t16.txt
    0.18943240503469277
    ./compute_perf_stats.py deltasvm_out/combined_positives_gkmsvm_t2_l10_k6_d3_t16.txt deltasvm_out/combined_negatives_gkmsvm_t2_l10_k6_d3_t16.txt 
    0.18795144871293468

Note that the deltaSVM authors also made lmer weights downloadable from their website, although to my knowledge they did not provide the models themselves. The weights they provided were derived through a combination of models trained on the five negative sets. When I applied these weights to score the dsQTLs with the command `./compute_perf_stats.py deltasvm_out/positives_deltasvmpaper.txt deltasvm_out/negatives_deltasvmpaper.txt`, I got an auPRC of `0.19338305610230075`, roughly consistent with the lsgkm paper (Supplementary Figure S5 gives an auPRC of 0.190). The text of the deltaSVM papers states that the models were trained with a "word length l = 10, informative columns k = 6 and truncated filter d = 3", which are the same as the parameters used to train the gkm SVMs here, although the software used was likely the original gkm implementation rather than lsgkm. 

See ReproduceFigure9.ipynb for code to reproduce Figure 9 in the paper.
