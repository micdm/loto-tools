#!/bin/bash

PAGES=$1
ACCOUND_ID=$2
COOKIES=$3
CSRF_TOKEN=$4

for PAGE in `seq $PAGES`; do
    curl -X POST https://btc-e.nz/ajax/billing -b "$COOKIES" -d "csrfToken=$CSRF_TOKEN&&act=history&id=$ACCOUNT_ID&page=$PAGE&view=1&type=1" > ../data/history$PAGE.html
    ./parser.py ../data/history$PAGE.html
done > ../data/history.data

./merger.py ../data/history.data > ../data/history.merged.data
