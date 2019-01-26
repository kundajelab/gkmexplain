#!/usr/bin/env python
from __future__ import division, print_function, absolute_import
import os
import shap #v 0.28.3
import numpy as np
import sys
import deeplift
from deeplift import dinuc_shuffle
import time
import random
import argparse
from glob import glob
from joblib import Parallel, delayed
import time


def onehot_seq(seq):
  letter_to_index = {'A':0, 'a':0,
                     'C':1, 'c':1,
                     'G':2, 'g':2,
                     'T':3, 't':3}
  to_return = np.zeros((len(seq),4))
  for idx,letter in enumerate(seq):
    to_return[idx,letter_to_index[letter]] = 1
  return to_return


def get_shap_explanation(gkmsvm_model_path,
                         seq, background_seqs,
                         tempfile, nsamples):
    start = time.time()  
    index_to_letter = {0:'A', 1:'C', 2:'G', 3:'T'}
    letter_to_index = dict([(y,x) for (x,y) in index_to_letter.items()])
  
    def pred_func(numerically_encoded_seqs):
        #convert the sequences to strings]
        seqs = ["".join(index_to_letter[x] for x in seq)
            for seq in numerically_encoded_seqs]
    
        tmpseqsfile = tempfile+"seqs.fa"
        fh = open(tmpseqsfile, "w")
        for i,seq in enumerate(seqs):
            fh.write(">seq"+str(i)+"\n")
            fh.write(seq+"\n")
        fh.close()
    
        model_preds = tempfile+"_shap_preds"
    
        os.system("lsgkm/src/gkmpredict -v 1 "+tmpseqsfile+" "
                  +gkmsvm_model_path+" "+model_preds)
    
        to_return = np.array([float(x.rstrip().split("\t")[1])
                             for x in open(model_preds)])
        os.remove(tmpseqsfile)
        os.remove(model_preds)
        return to_return
  
  
    X_test = np.array([letter_to_index[x] for x in seq])
  
    explainer = shap.KernelExplainer(pred_func,
                                   np.array(
                                   [[letter_to_index[x] for x in seq]
                                    for seq in background_seqs]
                                   ))
    shap_values = explainer.shap_values(X_test,
                                        nsamples=nsamples)
    print("tempfile",tempfile, time.time()-start)

    return shap_values[:,None]*onehot_seq(seq)


def run_me(args):
    input_file = args.input_fa
    model_file_path = args.model_file_path
    n_jobs = args.n_jobs
    n_bg = args.n_bg 
    nsamples = args.n_samples
    output_file_prefix = args.output_file_prefix
    tempfile = args.tempfile_prefix

    sequences = [x.rstrip() for (i,x) in enumerate(open(input_file))
                 if i%2==1]

    shap_imp_scores = Parallel(n_jobs=args.n_jobs)(
        delayed(get_shap_explanation)(
          gkmsvm_model_path=model_file_path,
          seq=the_seq,
          background_seqs=[
              dinuc_shuffle.dinuc_shuffle(the_seq)
              for j in range(n_bg)],
          tempfile=tempfile+str(i),
          nsamples=nsamples)
        for (i,the_seq) in enumerate(sequences))

    np.save(output_file_prefix, np.array(shap_imp_scores))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_fa", required=True) 
    parser.add_argument("--model_file_path", required=True)
    parser.add_argument("--n_jobs", type=int, required=True)
    parser.add_argument("--n_bg", type=int, required=True)
    parser.add_argument("--n_samples", type=int, required=True)
    parser.add_argument("--output_file_prefix",
                        type=str, required=True)
    parser.add_argument("--tempfile_prefix", default="tmpshap")
    run_me(parser.parse_args())
