#!/bin/bash

# Generates the maximum credibility clade trees
# Requires treeannotator

for LOG in $(find . -name 'beast.log'); do 
    DIR=$(dirname $LOG)
    NAME=$(basename $DIR)
    OUTPUT=$DIR/$NAME.subyz-rates.pdf
    
    if [[ $DIR == *"-subyz-"* ]]; then
        python plotsubyz.py $LOG $OUTPUT
    fi
done