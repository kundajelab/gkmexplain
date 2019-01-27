#Train the model with
./train_model.sh
./run_gkmexplain.py
./run_ism.py
./run_shap.py --input_fa test_positives.fa --model_file_path params_t3_l6_k5_d1_g2_c10_w3.model.txt --n_jobs 20 --n_bg 20 --n_samples 2000 --output_file_prefix shap2000_bg20_imp_scores
./run_shap.py --input_fa test_positives.fa --model_file_path params_t3_l6_k5_d1_g2_c10_w3.model.txt --n_jobs 20 --n_bg 20 --n_samples 20000 --output_file_prefix shap20000_bg20_imp_scores
./run_shap.py --input_fa test_positives.fa --model_file_path params_t3_l6_k5_d1_g2_c10_w3.model.txt --n_jobs 20 --n_bg 200 --n_samples 2000 --output_file_prefix shap2000_bg200_imp_scores


#Some PER SEQUENCE runtimes for shap @ 20000 samples, bg 20:
#tempfile tmpshap383 1114.14712
#tempfile tmpshap384 1104.38538504
#tempfile tmpshap386 1100.55476594
#tempfile tmpshap385 1101.92370105
#tempfile tmpshap387 1092.35954809
#tempfile tmpshap388 1096.70650315
#tempfile tmpshap389 1059.40146208
#tempfile tmpshap390 1104.89526892
#tempfile tmpshap392 1066.18015099
#tempfile tmpshap391 1099.12381005
#tempfile tmpshap393 1089.02405214
#tempfile tmpshap395 1071.51022816
#tempfile tmpshap396 1072.81696701
#tempfile tmpshap394 1102.33714581
#tempfile tmpshap397 1070.84324884
#tempfile tmpshap398 1060.13797903
#tempfile tmpshap399 1060.57516599

#Some PER SEQUENCE runtimes for shap @ 20000 samples, bg 200:
#tempfile tmpshap385 1120.66112399
#tempfile tmpshap387 1108.914886
#tempfile tmpshap389 1112.23420501
#tempfile tmpshap388 1124.84290314
#tempfile tmpshap391 1115.35765004
#tempfile tmpshap390 1118.41711092
#tempfile tmpshap392 1093.43674016
#tempfile tmpshap393 1097.42494988
#tempfile tmpshap394 1096.73449588
#tempfile tmpshap395 1095.51407194
#tempfile tmpshap396 1104.25273609
#tempfile tmpshap398 1095.15051079
#tempfile tmpshap397 1116.14081287
#tempfile tmpshap399 1101.66583991
