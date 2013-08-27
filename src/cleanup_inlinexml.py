#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script removes errors from MAX1270 inline XML formatted tokenized files,
where the files contain a certain HTML string that shouldn't be there:

</sentence><sentence>
Am
Ende
gehen
die
Wähler
vielleicht
nicht
mehr
an
die
Urnen
.
</sentence></paragraph><paragraph><sentence>
<font
class="fett">zum
<a
href="?loc=3_2&id=9471">Artikel</a>
</sentence></paragraph></file>
"""

import sys
import re

#~ regex = re.compile("</sentence></paragraph><paragraph><sentence>\n<font.*</a>\n", flags=re.MULTILINE|re.DOTALL)
regex = re.compile("<sentence>\n-<font.*</sentence>", flags=re.MULTILINE|re.DOTALL)

if __name__ == '__main__':
    in_fpath = sys.argv[1]
    with open(in_fpath, 'r') as in_file:
        input_str = in_file.read()
        result = regex.search(input_str)
        
    if result:
        output_str = ''.join(regex.split(input_str))
        with open(in_fpath, 'w') as out_file:
            out_file.write(output_str)
