#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann
#
# Purpose: Converts a file with one-word-per-line formatting (where sentences
# are separated by an empty line) into a one-sentence-per-line format.

import sys
import codecs

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: {0} one-word-per-line-input.txt one-sentence-per-line-output.txt".format(sys.argv[0])
        sys.exit(1)
    else:
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        with codecs.open(input_file_path, 'r', 'utf8') as input_file, \
        codecs.open(output_file_path, 'w', 'utf8') as output_file:
            for sentence in input_file.read().split('\n\n'):
                output_file.write(' '.join(sentence.split('\n'))+'\n')
