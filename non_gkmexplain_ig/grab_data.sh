#!/usr/bin/env bash

FILE="sequences.simdata.gz"
if [ ! -f "$FILE" ]
then
    wget https://github.com/AvantiShri/model_storage/raw/db919b12f750e5844402153233249bb3d24e9e9a/deeplift/genomics/sequences.simdata.gz
else
    echo "File sequences.simdata.gz exists already"
fi
