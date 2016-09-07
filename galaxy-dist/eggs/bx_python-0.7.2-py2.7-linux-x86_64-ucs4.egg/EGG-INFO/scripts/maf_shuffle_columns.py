#!/afs/bx.psu.edu/project/pythons/py2.7-linux-x86_64-ucs4/bin/python2.7

"""
Randomly shuffle the columns of each block of a maf file. Note that this does
not change any other features of the maf block, thus the text of each row no
longer will match the sequence refered to by the other row attributes!

usage: %prog < maf > maf
"""

import psyco_full

import sys

import sys
from bx import align

def __main__():

    maf_reader = align.maf.Reader( sys.stdin )
    maf_writer = align.maf.Writer( sys.stdout )

    for m in maf_reader:
    
        align.shuffle_columns( m )

        maf_writer.write( m )

if __name__ == "__main__": __main__()
