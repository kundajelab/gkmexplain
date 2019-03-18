#!/usr/bin/env python
from sklearn.metrics import roc_auc_score

pos_preds = [float(x.rstrip().split("\t")[1])
             for x in open("preds_test_positives.txt")]
neg_preds = [float(x.rstrip().split("\t")[1])
             for x in open("preds_test_negatives.txt")]
print(roc_auc_score(y_true=[1 for x in pos_preds]+[0 for x in neg_preds],
                    y_score = pos_preds+neg_preds))
