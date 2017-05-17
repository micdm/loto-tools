#!/bin/bash

./converter.py ../data/merged.data > data/dataset.csv
./model.py data/dataset.csv data/model.hdf5
./server.py data/model.hdf5
