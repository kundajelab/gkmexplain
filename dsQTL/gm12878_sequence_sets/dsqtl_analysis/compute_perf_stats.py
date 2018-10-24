#!/usr/bin/env python
from __future__ import division, print_function
import argparse
from sklearn.metrics import roc_auc_score
from sklearn.metrics import average_precision_score
import numpy as np

def run_me(args):
    
    pos_vals = [np.abs(float(x.rstrip().split("\t")[1])) for x in open(args.posfile)]
    neg_vals = [np.abs(float(x.rstrip().split("\t")[1])) for x in open(args.negfile)]

    preds = pos_vals+neg_vals
    true = [1 for x in pos_vals]+[-1 for x in neg_vals]
    print("auROC:",roc_auc_score(y_true=true, y_score=preds))
    print("auPRC:",average_precision_score(y_true=true, y_score=preds))

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("posfile")
    parser.add_argument("negfile")
    run_me(parser.parse_args())

