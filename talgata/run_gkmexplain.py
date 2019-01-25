#!/usr/bin/env python
import os
import numpy as np

model_file = "params_t3_l6_k5_d1_g2_c10_w3.model.txt"
os.system("lsgkm/src/gkmexplain test_positives.fa "+model_file+" explanation_positives.txt")
impscores = np.array([
    np.array(
        [[float(z) for z in y.split(",")]
        for y in x.rstrip().split("\t")[2].split(";")])
    for x in open("explanation_positives.txt")
])
print(impscores.shape)
np.save("gkmexplain_imp_scores", impscores)
