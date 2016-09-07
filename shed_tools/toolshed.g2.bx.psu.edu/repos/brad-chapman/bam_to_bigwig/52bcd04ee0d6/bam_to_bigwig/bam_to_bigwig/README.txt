Convert a BAM file into a BigWig coverage file. This can be used directly from 
Galaxy for display at UCSC. The advantage over standard Wiggle format is that 
the data is stored in a compressed format and can be retrieved by genome
region. This allows you to view regions of arbitrarily large Wiggle file data
at UCSC while avoiding the upload costs.

History
-------

v0.1.1 passes the forgotten split argument and moves to using the new
sub-command enabled bedtools. Thanks to David Leader.

As of v0.1.0, the Galaxy tools uses a revised bam_to_bigwig.py script using
genomeCoverageBed and bedGraphToBigWig - this approach allows gaps/skpis to
be excluded from the coverage calculation, which is important for RNA-Seq.

Until v0.0.2, this Galaxy tool used the bam_to_wiggle.py script from
https://github.com/chapmanb/bcbb/blob/master/nextgen/scripts/bam_to_wiggle.py
which internally used pysam (and thus samtools) and wigToBigWig from UCSC.

Requirements
------------

If you are installing this tool manually, place the Python script in the
same directory as the XML configuration file, or provide a soft link to it.
Ensure the following command line tools are on the system path:

pysam - Python interface to samtools (http://code.google.com/p/pysam/)
genomeCoverageBed - part of BedTools (http://code.google.com/p/bedtools/)
bedGraphToBigWig  - from UCSC (http://hgdownload.cse.ucsc.edu/admin/exe/)

Credits
-------

Original script by Brad Chapman, revisions from Peter Cock including the
switch to using genomeCoverageBed and bedGraphToBigWig based on the work
of Lance Parsons.

License
------

The code is freely available under the MIT license:
http://www.opensource.org/licenses/mit-license.html
