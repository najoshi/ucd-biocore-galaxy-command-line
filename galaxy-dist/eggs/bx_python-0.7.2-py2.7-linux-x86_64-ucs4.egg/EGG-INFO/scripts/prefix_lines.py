#!/afs/bx.psu.edu/project/pythons/py2.7-linux-x86_64-ucs4/bin/python2.7

"""
Simple script to add a prefix to every line in a file.
"""

import sys

for line in sys.stdin: print sys.argv[1] + line,
