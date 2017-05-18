#!/bin/bash

COUNT=$1
BET_MAKER="$2"

echo "Converting..."
./converter.py main ../data/merged.data > data/dataset.csv
for ROUND in `seq $COUNT`; do
    echo "Try #$ROUND"
    echo "Building model..."
    ./model.py data/dataset.csv data/model$ROUND.hdf5 > /dev/null 2>&1
    echo "Model ready"
    echo "Starting server..."
    ./server.py data/model$ROUND.hdf5 > /dev/null 2>&1 &
    PID=$!
    sleep 3
    echo "Server started"
    echo "Testing..."
    $BET_MAKER test ../data/merged.data 6 | grep "Win rate" &
    sleep 5
    kill -9 $PID
    wait $PID 2>/dev/null
    echo "Try complete!"
done
