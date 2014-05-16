#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This scripts converts tokenized text (one word per line = OWPL) with an
empty line between sentences into the CoNLL2009 format (as it is used by
mate-tools).
"""

import os
import errno
import sys

def extract_sentences(owpl_filepath):
    with open(owpl_filepath, 'r') as owpl_filepath:
        owpl_str = owpl_filepath.read()
        return owpl_str.split('\n\n')
        
def convert_sentences(owpl_sentences):
    """
    convert a list of OWPL formatted sentence strings into a list of
    CoNLL2009 formatted sentence strings
    """
    conll_sentences = []
    for owpl_sentence in owpl_sentences:
        if owpl_sentence: # last one might be empty
            conll_sentence = ''
            for i, word in enumerate(owpl_sentence.split('\n')):
                conll_word = '{0}\t{1}'.format(i, word) + '\t_' * 13 + '\n'
                conll_sentence += conll_word
            # sentences are separated by an empty line
            conll_sentences.append(conll_sentence + '\n')
    return conll_sentences
    
def write_sentences(conll_sentences, conll_filepath):
    with open(conll_filepath, 'w') as out_file:
        out_file.writelines(conll_sentences)

def create_dir(path):
    """
    Creates a directory. Warns, if the directory can't be accessed.
    Passes, if the directory already exists.

    @author: tzot (http://stackoverflow.com/a/600612)
    @param path: path to the directory to be created
    @type path: C{str}
    """
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        elif exc.errno == errno.EACCES:
            print "Cannot create [%s]! Check Permissions" % path
        else:
            raise


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: %s input_file output_file' % sys.argv[0])
        sys.exit(1)
    else:
        input_file = sys.argv[1]
        owpl_sentences = extract_sentences(input_file)
        conll_sentences = convert_sentences(owpl_sentences)
        output_file = sys.argv[2]
        output_dir = os.path.dirname(output_file)
        create_dir(output_dir)
        write_sentences(conll_sentences, output_file)
