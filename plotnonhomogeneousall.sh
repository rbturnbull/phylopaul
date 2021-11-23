#!/bin/bash

# Generates the maximum credibility clade trees
# Requires treeannotator

for LOG in $(find . -name 'beast.log'); do 
    DIR=$(dirname $LOG)
    NAME=$(basename $DIR)
    OUTPUT=$DIR/$NAME.nonhomogeneous.pdf
    
    if [[ $DIR == *"-nonhomogeneous" ]]; then
        python plotnonhomogeneous.py $LOG $OUTPUT
    fi
done