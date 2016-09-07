#!/usr/bin/env python

import optparse, os, shutil, subprocess, sys, tempfile

def stop_err( msg ):
    sys.stderr.write( '%s\n' % msg )
    sys.exit()

def __main__():
    #Parse Command Line
    parser = optparse.OptionParser()
    parser.add_option( '-g', dest='ref_annotation', help='An optional "reference" annotation GTF. Each sample is matched against this file, and sample isoforms are tagged as overlapping, matching, or novel where appropriate. See the refmap and tmap output file descriptions below.' )
    parser.add_option( '-s', dest='use_seq_data', action="store_true", help='Causes cuffmerge to look into for fasta files with the underlying genomic sequences (one file per contig) against which your reads were aligned for some optional classification functions. For example, Cufflinks transcripts consisting mostly of lower-case bases are classified as repeats. Note that <seq_dir> must contain one fasta file per reference chromosome, and each file must be named after the chromosome, and have a .fa or .fasta extension.')
    parser.add_option( '-p', '--num-threads', dest='num_threads', help='Use this many threads to align reads. The default is 1.' )
    
    # Wrapper / Galaxy options.
    parser.add_option( '', '--index', dest='index', help='The path of the reference genome' )
    parser.add_option( '', '--ref_file', dest='ref_file', help='The reference dataset from the history' )
    
    # Outputs.
    parser.add_option( '', '--merged-transcripts', dest='merged_transcripts' )
    parser.add_option( '--min-isoform-fraction', dest='min_isoform_fraction' )
    
    (options, args) = parser.parse_args()
    
    # output version # of tool
    try:
        tmp = tempfile.NamedTemporaryFile().name
        tmp_stdout = open( tmp, 'wb' )
        proc = subprocess.Popen( args='cuffmerge -v 2>&1', shell=True, stdout=tmp_stdout )
        tmp_stdout.close()
        returncode = proc.wait()
        stdout = None
        for line in open( tmp_stdout.name, 'rb' ):
            if line.lower().find( 'merge_cuff_asms v' ) >= 0:
                stdout = line.strip()
                break
        if stdout:
            sys.stdout.write( '%s\n' % stdout )
        else:
            raise Exception
    except:
        sys.stdout.write( 'Could not determine Cuffmerge version\n' )
        
    # Set/link to sequence file.
    if options.use_seq_data:
        if options.ref_file:
            # Sequence data from history.
            # Create symbolic link to ref_file so that index will be created in working directory.
            seq_path = "ref.fa"
            os.symlink( options.ref_file, seq_path  )
        else:
            if not os.path.exists( options.index ):
                stop_err( 'Reference genome %s not present, request it by reporting this error.' % options.index )
            seq_path = options.index
    
    # Build command.
    
    # Base.
    cmd = "cuffmerge -o cm_output "
    
    # Add options.
    if options.num_threads:
        cmd += ( " -p %i " % int ( options.num_threads ) )
    if options.ref_annotation:
        cmd += " -g %s " % options.ref_annotation
    if options.use_seq_data:
        cmd += " -s %s " % seq_path
    if options.min_isoform_fraction:
        cmd += " --min-isoform-fraction %s " % (options.min_isoform_fraction)
    # Add input files to a file.
    inputs_file_name = tempfile.NamedTemporaryFile( dir="." ).name
    inputs_file = open( inputs_file_name, 'w' )
    for arg in args:
        inputs_file.write( arg + "\n" )
    inputs_file.close()
    cmd += inputs_file_name

    # Debugging.
    print cmd
    
    # Run command.
    try:        
        tmp_name = tempfile.NamedTemporaryFile( dir="." ).name
        tmp_stderr = open( tmp_name, 'wb' )
        proc = subprocess.Popen( args=cmd, shell=True, stderr=tmp_stderr.fileno() )
        returncode = proc.wait()
        tmp_stderr.close()
        
        # Get stderr, allowing for case where it's very large.
        tmp_stderr = open( tmp_name, 'rb' )
        stderr = ''
        buffsize = 1048576
        try:
            while True:
                stderr += tmp_stderr.read( buffsize )
                if not stderr or len( stderr ) % buffsize != 0:
                    break
        except OverflowError:
            pass
        tmp_stderr.close()
        
        # Error checking.
        if returncode != 0:
            raise Exception, stderr
            
        if len( open( "cm_output/merged.gtf", 'rb' ).read().strip() ) == 0:
            raise Exception, 'The output file is empty, there may be an error with your input file or settings.'
            
        # Copy outputs.
        shutil.copyfile( "cm_output/merged.gtf" , options.merged_transcripts )    
            
    except Exception, e:
        stop_err( 'Error running cuffmerge. ' + str( e ) )
        
if __name__=="__main__": __main__()
