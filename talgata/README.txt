#Train the model with
./train_model.sh
./run_gkmexplain.py
./run_ism.py
./run_shap.py --input_fa test_positives.fa --model_file_path params_t3_l6_k5_d1_g2_c10_w3.model.txt --n_jobs 20 --n_bg 20 --n_samples 2000 --output_file_prefix shap2000_bg20_imp_scores
