#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann
#
# Purpose: reads tokenized text (whitespace separated),
# writes one-word-per-line output (with sentences separated by an empty line)

import sys
import re
import argparse

PARAGRAPH_SPLIT_REGEX = re.compile('\n\n')

# sentence endings in tokenized text, e.g. ' . ' or ' ! '
SENTENCE_SPLIT_REGEX = re.compile(' (\.|!|\?|) ')

# In the legacy corpora I have to deal with, words are sometimes separated
# by a whitespace soft-hyphen whitespace combination.
# if that's not the case, simply split after one whitespace
WORD_SPLIT_REGEX = re.compile(' \xc2\xad | ')


def split_paragraphs(input_string, segmentation_marker):
    return re.sub(PARAGRAPH_SPLIT_REGEX, ' {}'.format(segmentation_marker),
                  input_string)


def split_sentences(input_string, segmentation_marker):
    """
    reads a string and appends the given segmentation marker to the end of each
    sentence (e.g. '\n\n' or '<EOS>'.
    """
    return re.sub(SENTENCE_SPLIT_REGEX, r' \1{}'.format(segmentation_marker),
                  input_string)


def one_sentence_per_line(input_string, segmentation_marker='\n\n'):
    """
    produces a (generator of a) list of strings, where each string contains
    a sentence. Each sentence/string ends with the given segmentation
    marker.
    """
    marked_paras_str = split_paragraphs(input_string, segmentation_marker)
    marked_sents_str = split_sentences(marked_paras_str, segmentation_marker)
    # produce one sentence per line
    return (line.strip() for line in marked_sents_str.splitlines())


def one_word_per_line(input_string, segmentation_marker='\n\n',
                      output_format='owpl'):
    """
    produces a list of strings, where each string contains a single word.
    There'll be one additional string containing the segmentation marker after
    each sentence.
    """
    assert output_format in ('owpl', 'conll2009', 'conllx')
    marked_paras_str = split_paragraphs(input_string, segmentation_marker)
    marked_sents_str = split_sentences(marked_paras_str, segmentation_marker)
    # produce one word per line, with sentences separated by an empty line
    owpl = re.split(WORD_SPLIT_REGEX, marked_sents_str)
    output = []
    if output_format == 'owpl':
        output = owpl
    else:  # output_format in ('conll2009', 'conllx'):
        if output_format == 'conll2009':
            num_empty_cols = 13
        elif output_format == 'conllx':
            num_empty_cols = 8
        
        output = []
        word_id = 1
        for line in owpl:
            word = line.strip()
            if word:
                output.append("{}\t{}{}".format(word_id, word,
                                              '\t_'*num_empty_cols))
                word_id += 1
            else:
                output.append("\n")
                word_id = 1
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--output_format', default='owpl',
                        help=('owpl (one-word-per-line), '
                              'ospl (one-sentence-per-line),'
                              'conll2009 or conllx.'
                              'default: owpl'))
    parser.add_argument('-s', '--segmentation_marker', default='\n\n',
                        help=("The segmentation marker is added after each "
                              "sentence. default: '\n\n'"))
    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('output_file', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout)
    args = parser.parse_args(sys.argv[1:])

    input_string = args.input_file.read()

    if args.output_format in ('owpl', 'conll2009', 'conllx'):
        lines = one_word_per_line(input_string, args.segmentation_marker,
                                  args.output_format)
    elif args.output_format == 'ospl':
        lines = one_sentence_per_line(input_string,
                                      args.segmentation_marker)

    for line in lines:
        args.output_file.write(line + '\n')
