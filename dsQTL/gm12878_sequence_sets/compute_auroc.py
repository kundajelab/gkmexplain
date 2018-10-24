#!/usr/bin/env python
from __future__ import division
import argparse
from sklearn.metrics import roc_auc_score


def compute_auroc(args):
    predictions = []
    labels = []
    for line in open(args.cvpred_file):
        region,pred,label,fold = line.rstrip().split("\t")
        pred = float(pred)
        label = int(label)
        predictions.append(pred)
        labels.append(label)
    print(roc_auc_score(y_true=labels, y_score=predictions)) 


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Compute auroc for cvpred file")
    parser.add_argument('cvpred_file')
    args = parser.parse_args()
    compute_auroc(args)
    
