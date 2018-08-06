#!/usr/bin/env bash

python generate_synthetic_sequences.py

gzip sequences.simdata

zcat sequences.simdata.gz | perl -lane 'if (substr($F[0], 0, 9) eq "gata_tal1") {print ">".$F[0]."\n".$F[1]}' | gzip -c > positives.fa.gz

zcat sequences.simdata | perl -lane 'if ($. > 1 && (substr($F[0], 0, 9) ne "gata_tal1")) {print ">".$F[0]."\n".$F[1]}' | gzip -c > negatives.fa.gz
