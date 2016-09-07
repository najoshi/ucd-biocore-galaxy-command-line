#! /usr/bin/env python
import screed
import sys
import os.path

def is_pair(name1, name2):
    if name1.endswith('/1') and name2.endswith('/2'):
        s1 = name1.split('/')[0]
        s2 = name2.split('/')[0]
        if s1 == s2:
            assert(s1)
            return True
        
    return False

infile = sys.argv[1]
outfile = os.path.basename(infile)
if len(sys.argv) > 3:
    outfile1 = sys.argv[2]
    outfile2 = sys.argv[3]

single_fp = open(outfile1, 'w')
paired_fp = open(outfile2, 'w')

last_record = None
last_name = None

n_pe = 0
n_se = 0

print 'splitting pe/se sequences from %s to %s.{pe,se}' % (infile, outfile)
for n, record in enumerate(screed.open(sys.argv[1])):
    if n % 100000 == 0 and n > 0:
       print '...', n
    name = record['name'].split()[0]
    sequence = record['sequence']

    if last_record:
        if is_pair(last_name, name):
           print >>paired_fp, '>%s\n%s' % (last_name, last_record['sequence'])
           print >>paired_fp, '>%s\n%s' % (name, record['sequence'])
           name, record = None, None
           n_pe += 1
        else:
           print >>single_fp, '>%s\n%s' % (last_name, last_record['sequence'])
           n_se += 1

    last_name = name
    last_record = record

if last_record:
    if is_pair(last_name, name):
        print >>paired_fp, '>%s\n%s' % (last_name, last_record['sequence'])
        print >>paired_fp, '>%s\n%s' % (name, record['sequence'])
        name, record = None, None
        n_pe += 1
    else:
        print >>single_fp, '>%s\n%s' % (last_name, last_record['sequence'])
        name, record = None, None
        n_se += 1

if record:
   print >>single_fp, '>%s\n%s' % (name, record['sequence'])
   n_se += 1

single_fp.close()
paired_fp.close()

if n_pe == 0:
    raise Exception("no paired reads!? check file formats...")
    
print 'DONE; read %d sequences, %d pairs and %d singletons' % \
      (n + 1, n_pe, n_se)
