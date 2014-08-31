# Usage: turboparser_german.sh tokenized.input conllx-dependency-parsed.output
# Purpose: parses a pre-tokenized file with TurboParser (and the German
#          language model trained on the Tiger corpus)

mkdir -p tmp
./toktxt2owpl.py -s '<EOS>\n' $1 | tree-tagger-german | ./treetagger2conllx.py > tmp/conllx.input

$TURBOPARSER_HOME/TurboParser --test \
--file_model=$TURBOPARSER_HOME/models/tiger_release_aug07.model \
--file_test=tmp/conllx.input \
--file_prediction=$2 \
