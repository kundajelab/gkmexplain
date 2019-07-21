
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

