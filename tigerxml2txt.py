#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann
#
# Purpose: extracts sentences from a Tiger XML input file and writes
#          them to an output file (one word per line with an empty line
#          between sentences).

import sys
import codecs
from lxml import etree

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: {0} tiger_input.xml plain_output.txt".format(sys.argv[0])
        sys.exit(1)
    else:
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        tree = etree.parse(input_file_path)
        with codecs.open(output_file_path, 'w', 'utf8') as output_file:
            for sent in tree.iterfind('//s'):
                for token in sent.iterfind('./graph/terminals/t'):
                    output_file.write(token.attrib['word']+'\n')
                output_file.write('\n')
