#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann

# Purpose: reads TreeTagger output files and converts them into CoNLL-X format

import sys
import re
import argparse

def treetagger2conllx(input_file, output_file, segmentation_marker):
    """
    reads a TreeTagger file (3 columns: token, pos, lemma) and writes a
    CoNLL-X file. All unknown columns in the output will be filled with '_'.
    """
    lines = input_file.readlines()
    segmentation_line = segmentation_marker+'\n'
    word_id = 1
    for line in lines:
        stripped_line = line.strip()
        if stripped_line and line != segmentation_line:
            try:
                token, pos, lemma = line.split()
                output_file.write("{0}\t{1}\t{2}\t{3}\t{3}\t_\t_\t_\t_\t_\n".format(word_id, token, lemma, pos))
                word_id += 1
            except ValueError as e:
                sys.stderr.write(("{}\nDid you specify the segmentation "
                                  "marker? The line contains this: {}\n".format(e, line)))
        else:  # we've reached the end of a sentence or paragraph
            output_file.write('\n')
            word_id = 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--segmentation_marker', default='<EOS>',
                        help=("The segmentation marker (end-of-sentence marker)"
                              " used by TreeTagger. default: <EOS>"))
    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('output_file', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout)
    args = parser.parse_args(sys.argv[1:])

    treetagger2conllx(args.input_file, args.output_file, args.segmentation_marker)
