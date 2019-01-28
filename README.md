# Fast and Accurate Interpretation of Nonlinear Gapped k-mer SVMs

This repository accompanies [Gkmexplain: Fast and Accurate Interpretation of Nonlinear Gapped k-mer Support Vector Machines Using Integrated Gradients](https://www.biorxiv.org/content/early/2018/11/06/457606) by Shrikumar\*†, Prakash\* and Kundaje† (\*co-first authors †co-corresponding authors).

Please see [https://github.com/kundajelab/igsvm/blob/master/lsgkmexplain_TALGATA.ipynb](https://github.com/kundajelab/igsvm/blob/master/lsgkmexplain_TALGATA.ipynb) and [https://github.com/kundajelab/igsvm/blob/master/lsgkmexplain_NFE2.ipynb](https://github.com/kundajelab/igsvm/blob/master/lsgkmexplain_NFE2.ipynb) for example notebooks demonstrating usage on simulated and real genomic data, respectively.

Please see https://github.com/kundajelab/gkmexplain/tree/master/dsQTL for scripts to replicate the dsQTL analysis.

Please see https://github.com/kundajelab/gkmexplain/tree/master/talgata for scripts to replicate the ananlysis on the simulated sequences containing TAL1 and GATA motifs.

The code that implements the gkmexplain interpretation method (for genomic sequences) is at https://github.com/kundajelab/lsgkm (see gkmexplain.c under "src").

An example of using Integrated Gradients on a non-genomics dataset (the Madelon dataset) is at https://colab.research.google.com/drive/1LUGMIwOHLKDdK3deg7IIZ71kb2Nu1qv2
