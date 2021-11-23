#!/bin/bash

# Generates the maximum credibility clade trees
# Requires treeannotator

for TREES in $(find . -name '*.trees'); do 
    DIR=$(dirname $TREES)
    NAME=$(basename $DIR)
    OUTPUT=$DIR/$NAME.maxclade.tree
    echo $OUTPUT
    treeannotator -burnin 50 -heights mean $TREES $OUTPUT
done