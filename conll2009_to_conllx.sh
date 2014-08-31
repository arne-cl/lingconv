#!/bin/sh
# Purpose: convert a CoNLL2009 formatted file into CoNLL-X format
# Usage: ./conll2009_to_conllx.sh < input.conll2009 > output.conllx
#
# Note: There's no CPOSTAG column in CoNLL2009 format, so POSTAG is used twice.
#       awk will generate lines consisting of lots of \t for each empty input line.
#       this is what the perl part filters out
awk -F '\t' -v OFS='\t' '{print $1, $2, $3, $5, $5, $7, $9, $11, $10, $12}' | perl -pe 's/^\t\t\t\t\t\t\t\t\t$//'