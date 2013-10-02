#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script converts the inline XML tokenization format used for
MAZ1270 to the more conventional one-token-per-line (with empty lines 
between sentences) format.

MAZ1270 example:
<?xml version='1.0' encoding='ISO-8859-1'?>
<file>
<paragraph>
<sentence>
Dagmar
Ziegler
sitzt
in
der
Schuldenfalle
.
</sentence><sentence>
Der
Rückzieher
der
Finanzministerin
ist
aber
verständlich
.
</sentence>
</paragraph>
</file>
"""

import re
import os
import sys
import errno
import codecs
from bs4 import UnicodeDammit
from lxml import etree


SOFT_HYPHEN_RE = re.compile('\xc2\xad') # (mostly) invisible char

def remove_soft_hyphen(input_str):
    """
    removes invisible soft-hyphens from a string.

    input: 'FOO\xc2\xadBAR'
    output: 'FOOBAR'
    """
    return re.sub(SOFT_HYPHEN_RE, '', input_str)

def abslistdir(directory):
    """
    returns a list of absolute filepaths for all files found in the given
    directory.
    """
    abs_dir = os.path.abspath(directory)
    filenames = os.listdir(abs_dir)
    return [os.path.join(abs_dir, filename) for filename in filenames]
    
    
def extract_sentences(xml_file):
    """
    returns all sentence strings extracted from a MAZ1270 formatted XML
    file.
    """
    try:
        xml_str = remove_soft_hyphen(open(xml_file, 'r').read())
        tree = etree.fromstring(xml_str)
        paragraphs = tree.findall('paragraph')
        sentences = []
        for para in paragraphs:
            for sent in para.findall('sentence'):
                # remove initial/trailing \n 
                stripped_sent = sent.text.strip()
                # remove empty lines that occur within a 
                # one-line-per-sentence tokenized sentence
                cleaned_sent = re.sub('\n{2,}', '\n', stripped_sent)
                sentences.append(cleaned_sent)
        return sentences
    except etree.XMLSyntaxError as e:
        print e.msg


def create_dir(path):
    """
    Creates a directory. Warns, if the directory can't be accessed. Passes,
    if the directory already exists.

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
    
def write_sentences(sentences, output_filepath):
    with open(output_filepath, 'w') as output:
        utf8_sents = [s.encode('utf8') for s in sentences 
                        if isinstance(s, unicode)]
        for sent in utf8_sents:
            output.write(sent + '\n\n')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write(
            ("Convert between *.tok.xml inline XML tokenized files and "
            "one-token-per-line format.\n"))
        sys.stderr.write("Usage %s input_dir output_dir\n" % sys.argv[0])
    else:
        input_dir = sys.argv[1]
        assert os.path.isdir(input_dir), '%s is not a directory\n' % input_dir
        output_dir = sys.argv[2]
        
        xml_filepaths = abslistdir(input_dir)
        for xml_filepath in xml_filepaths:
            if xml_filepath.endswith(".tok.xml"): # ignore README etc.
                print "converting %s ..." % xml_filepath
                sentences = extract_sentences(xml_filepath)
                create_dir(output_dir)
                # rename *.tok.xml to *.tok
                filename = os.path.basename(xml_filepath).rsplit('.xml', 1)[0]
                output_filepath = os.path.join(output_dir, filename)
                write_sentences(sentences, output_filepath)
