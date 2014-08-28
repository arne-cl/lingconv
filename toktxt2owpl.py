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


def read_tokenized_file(input_file):
    # sentence endings in tokenized text, e.g. ' . ' or ' ! '
    SENTENCE_SPLIT_REGEX = re.compile(' (\.|!|\?) ')

    # words are sometimes separated by a whitespace soft-hyphen whitespace combination
    # if that's not the case, simply split after one whitespace
    WORD_SPLIT_REGEX = re.compile(' \xc2\xad | ')

    # all sentence endings are signalled by '\n\n'
    text_with_newlines = re.sub(SENTENCE_SPLIT_REGEX, r' \1\n', input_file.read())
    #return text_with_newlines
    return re.split(WORD_SPLIT_REGEX, text_with_newlines)


def write_owpl(lines, output_file):
    """
    Writes the tokenized input to an one-word-per-line output file
    (with sentences separated by two newlines).

    Params
    ------
    lines : list of str
        list of strings which contain one word each
    """
    for line in lines:
        output_file.write(line + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=file, default=sys.stdin)
    parser.add_argument('output_file', nargs='?', type=file, default=sys.stdout)
    args = parser.parse_args(sys.argv[1:])

    lines = read_tokenized_file(args.input_file)
    write_owpl(lines, args.output_file)

