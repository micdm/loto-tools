#!/bin/bash

echo "Parsing..."
for i in `find -L data -name "*.html"`; do 
    cache=$i.data
    if [ -f $cache ]; then
        cat $cache
    else
        (>&2 echo "Parsing $i")
        ./parser.py $i | tee $cache
    fi
done > data/parsed.data
echo "Merging..."
./merger.py data/parsed.data > data/merged.data
