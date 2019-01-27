#!/usr/bin/env bash 

run_shap_func () {
    prefix=$1 
    flanksize=$2
    n_bg=$3
    n_samples=$4

    outdir=shap_out"_bg"$n_bg"_samples"$n_samples
    [[ -e $outdir ]] || mkdir $outdir

    echo "On posmajor "$prefix
    ./run_shap_score_central_base.py\
     --input_fa "posmajor_"$flanksize"flank_coords.fa"\
     --model_file_path $prefix".model.txt"\
     --output_file $outdir"/pos_major_"$flanksize"_"$prefix".txt"\
     --n_jobs 20\
     --n_bg $n_bg\
     --n_samples $n_samples

    echo "On posminor "$prefix
    ./run_shap_score_central_base.py\
     --input_fa "posminor_"$flanksize"flank_coords.fa"\
     --model_file_path $prefix".model.txt"\
     --output_file $outdir"/pos_minor_"$flanksize"_"$prefix".txt"\
     --n_jobs 20\
     --n_bg $n_bg\
     --n_samples $n_samples

    echo "On negmajor "$prefix
    ./run_shap_score_central_base.py\
     --input_fa "negmajor_"$flanksize"flank_coords.fa"\
     --model_file_path $prefix".model.txt"\
     --output_file $outdir"/neg_major_"$flanksize"_"$prefix".txt"\
     --n_jobs 20\
     --n_bg $n_bg\
     --n_samples $n_samples

    echo "On negminor "$prefix
    ./run_shap_score_central_base.py\
     --input_fa "negminor_"$flanksize"flank_coords.fa"\
     --model_file_path $prefix".model.txt"\
     --output_file $outdir"/neg_minor_"$flanksize"_"$prefix".txt"\
     --n_jobs 20\
     --n_bg $n_bg\
     --n_samples $n_samples

    paste $outdir/"pos_major_"$flanksize"_"$prefix.txt $outdir/"pos_minor_"$flanksize"_"$prefix.txt | perl -lane 'print $F[0]."\t".($F[3]-$F[1])' > $outdir/"shap_diff_pos_"$flanksize"_"$prefix.txt
    paste $outdir/"neg_major_"$flanksize"_"$prefix.txt $outdir/"neg_minor_"$flanksize"_"$prefix.txt | perl -lane 'print $F[0]."\t".($F[3]-$F[1])' > $outdir/"shap_diff_neg_"$flanksize"_"$prefix.txt
}

nbg=20
nsamples=510
ln -s ~/lsgkm .

run_shap_func gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset1 51 $nbg $nsamples
run_shap_func gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset2 51 $nbg $nsamples
run_shap_func gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset3 51 $nbg $nsamples
run_shap_func gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset4 51 $nbg $nsamples
run_shap_func gkmsvm_t3_l10_k6_d3_c10_g2_t16_negset5 51 $nbg $nsamples

#sample runtime in seconds per variant...too slow...
#tempfile tmpshap18 538.429147005
#tempfile tmpshap22 457.31674099
#tempfile tmpshap20 506.442214012
#tempfile tmpshap23 481.180209875
#tempfile tmpshap25 486.616166115
#tempfile tmpshap29 483.115988016
#tempfile tmpshap21 511.701988935
#tempfile tmpshap24 501.044990063
#tempfile tmpshap28 492.650929928
#tempfile tmpshap30 490.272205114
#tempfile tmpshap27 503.60407114
#tempfile tmpshap33 499.681439161
#tempfile tmpshap26 514.861047983
#tempfile tmpshap36 495.08408308
#tempfile tmpshap35 504.993518114
#tempfile tmpshap32 516.512398005
#tempfile tmpshap38 489.978659153
#tempfile tmpshap34 518.840497971
#tempfile tmpshap37 504.62121892
#tempfile tmpshap31 529.60678196
#tempfile tmpshap39 508.553696156
