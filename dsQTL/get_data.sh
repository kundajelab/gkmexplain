#!/usr/bin/env bash

#download the data and move the dsqtl data into its own subdirectory
wget http://www.beerlab.org/deltasvm/downloads/gm12878_sequence_sets.tar.gz
tar -xzf gm12878_sequence_sets.tar.gz
cd gm12878_sequence_sets
mkdir dsqtl_analysis
mv dsqtl_test_* dsqtl_analysis

