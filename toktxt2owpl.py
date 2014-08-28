#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann
#
# Purpose: reads tokenized text (whitespace separated),
# writes one-word-per-line output (with sentences separated by an empty line)

import sys
import re
import os
import argparse


def parse_tokenized_file(input_file, split_sentences_only=False):
    # sentence endings in tokenized text, e.g. ' . ' or ' ! '
    SENTENCE_SPLIT_REGEX = re.compile(' (\.|!|\?) ')

    # words are sometimes separated by a whitespace soft-hyphen whitespace combination
    # if that's not the case, simply split after one whitespace
    WORD_SPLIT_REGEX = re.compile(' \xc2\xad | ')

    # produce one sentence per line
    if split_sentences_only:
        SENTENCE_SPLIT_REGEX = re.compile('(.*?(\.|!|\?) )')
        return re.split(SENTENCE_SPLIT_REGEX, input_file.read())
    # produce one word per line, with sentences separated by an empty line
    else:
        # all sentence endings are signalled by '\n\n'
        text_with_newlines = re.sub(SENTENCE_SPLIT_REGEX, r' \1\n\n', input_file.read())
        return re.split(WORD_SPLIT_REGEX, text_with_newlines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--split-only-sentences', action='store_true')
    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('output_file', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args(sys.argv[1:])

    for line in parse_tokenized_file(args.input_file, args.split_only_sentences):
        args.output_file.write(line + '\n')

