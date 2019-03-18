# GkmExplain Fast and Accurate Interpretation of Nonlinear Gapped k-mer Support Vector Machines

This repository accompanies [Gkmexplain: Fast and Accurate Interpretation of Nonlinear Gapped k-mer SVMs](https://www.biorxiv.org/content/early/2018/11/06/457606) by Shrikumar\*†, Prakash\* and Kundaje† (\*co-first authors †co-corresponding authors).

Please see [lsgkmexplain_TALGATA.ipynb](https://github.com/kundajelab/igsvm/blob/master/lsgkmexplain_TALGATA.ipynb) and [lsgkmexplain_Nanog.ipynb](https://github.com/kundajelab/igsvm/blob/master/lsgkmexplain_Nanog.ipynb) for example notebooks demonstrating usage on simulated and real genomic data, respectively.

Please see https://github.com/kundajelab/gkmexplain/tree/master/dsQTL for scripts to replicate the dsQTL analysis.

Please see https://github.com/kundajelab/gkmexplain/tree/master/talgata for scripts to replicate the ananlysis on the simulated sequences containing TAL1 and GATA motifs.

Please see https://github.com/kundajelab/gkmexplain/tree/master/Nanog_H1ESC for information on how to replicate the ananlysis on the Nanog data. Note that the notebook [lsgkmexplain_Nanog.ipynb](https://github.com/kundajelab/igsvm/blob/master/lsgkmexplain_Nanog.ipynb) contains the code to process the data, train the model, compute importance scores and run TF-MoDISco.

The code that implements the gkmexplain interpretation method (for genomic sequences) is at https://github.com/kundajelab/lsgkm (see gkmexplain.c under "src").

An example of using Integrated Gradients on a non-genomics dataset (the Madelon dataset) is at https://colab.research.google.com/drive/1LUGMIwOHLKDdK3deg7IIZ71kb2Nu1qv2
