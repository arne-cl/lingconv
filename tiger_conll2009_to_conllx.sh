#!/bin/sh
# Purpose: convert the TIGER treebank (in CoNLL2009 format) into CoNLL-X format
# Prerequisites: tiger2dep has to be used to convert TIGER into CoNLL2009 format
#
# Usage: ./conll2009_to_conllx.sh < tiger2dep_input.conll2009 > output.conllx
# Note: tiger2dep produces weird word IDs (SENTENCE-ID_WORD-ID instead of WORD-ID),
#       that's what perl filters out here in 's/^\d+_//'
awk -F '\t' -v OFS='\t' '{print $1, $2, $3, $5, $5, $7, $9, $11, $10, $12}' | perl -pe 's/^\d+_//' | perl -pe 's/^\t\t\t\t\t\t\t\t\t$//'
