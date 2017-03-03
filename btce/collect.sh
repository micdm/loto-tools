#!/bin/bash

echo "Parsing..."
for i in `find data -name "*.html"`; do ./parser.py $i; done > data/parsed.data
echo "Merging..."
./merger.py data/parsed.data > data/merged.data
