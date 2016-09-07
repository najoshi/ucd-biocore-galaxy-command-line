#!/afs/bx.psu.edu/project/pythons/py2.7-linux-x86_64-ucs4/bin/python2.7

"""
Print the number of bases in a nib file.

usage: %prog nib_file
"""

from bx.seq import nib as seq_nib
import sys

nib = seq_nib.NibFile( file( sys.argv[1] ) )
print nib.length
