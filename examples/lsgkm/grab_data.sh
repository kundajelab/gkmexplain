#!/usr/bin/env bash

FILE="ziptalgata.zip"
if [ ! -f "$FILE" ]
then
    wget https://github.com/evaprakash/lsgkm/blob/master/ziptalgata.zip?raw=true
    mv "ziptalgata.zip?raw=true" ziptalgata.zip
    unzip ziptalgata.zip
else
    echo "File ziptalgata.zip exists already"
fi
