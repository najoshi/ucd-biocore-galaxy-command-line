"""
CuffData 
"""
import logging
import os,os.path,sys,re
import tempfile
from subprocess import Popen
import galaxy.datatypes.data
from galaxy.datatypes.images import Html
from galaxy.datatypes.binary import Binary
from galaxy import util
from galaxy.datatypes.metadata import MetadataElement

log = logging.getLogger(__name__)

class CuffDiffData( Html ):
    """
    CuffDiff output files:
    run.info
    read_groups.info
    cds.count_tracking
    cds.diff
    cds.fpkm_tracking
    cds.read_group_tracking
    cds_exp.diff
    gene_exp.diff
    genes.count_tracking
    genes.fpkm_tracking
    genes.read_group_tracking
    isoform_exp.diff
    isoforms.count_tracking
    isoforms.fpkm_tracking
    isoforms.read_group_tracking
    promoters.diff
    splicing.diff
    tss_group_exp.diff
    tss_groups.count_tracking
    tss_groups.fpkm_tracking
    tss_groups.read_group_tracking
    """
    file_ext = 'cuffdata'
    is_binary = False
    composite_type = 'auto_primary_file'
    allow_datatype_change = False
    def __init__( self, **kwd ):
        Html.__init__( self, **kwd )
        self.add_composite_file('run.info', description = 'run.info', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('read_groups.info', description = 'read_groups.info', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('cds.count_tracking', description = 'cds.count_tracking', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('cds.diff', description = 'cds.diff', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('cds.fpkm_tracking', description = 'cds.fpkm_tracking', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('cds.read_group_tracking', description = 'cds.read_group_tracking', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('cds_exp.diff', description = 'cds_exp.diff', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('gene_exp.diff', description = 'gene_exp.diff', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('genes.count_tracking', description = 'genes.count_tracking', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('genes.fpkm_tracking', description = 'genes.fpkm_tracking', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('genes.read_group_tracking', description = 'genes.read_group_tracking', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('isoform_exp.diff', description = 'isoform_exp.diff', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('isoforms.count_tracking', description = 'isoforms.count_tracking', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('isoforms.fpkm_tracking', description = 'isoforms.fpkm_tracking', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('isoforms.read_group_tracking', description = 'isoforms.read_group_tracking', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('promoters.diff', description = 'promoters.diff', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('splicing.diff', description = 'splicing.diff', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('tss_group_exp.diff', description = 'tss_group_exp.diff', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('tss_groups.count_tracking', description = 'tss_groups.count_tracking', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('tss_groups.fpkm_tracking', description = 'tss_groups.fpkm_tracking', mimetype = 'text/html', optional = True, is_binary = False )
        self.add_composite_file('tss_groups.read_group_tracking', description = 'tss_groups.read_group_tracking', mimetype = 'text/html', optional = True, is_binary = False )

    def generate_primary_file( self, dataset = None ):
        """ 
        This is called only at upload to write the html file
        cannot rename the datasets here - they come with the default unfortunately
        """
        rval = ['<html><head><title>CuffDiff Output</title></head>']
        rval.append('<body>')
        rval.append('<p/>CuffDiff Outputs:<p/><ul>')
        for composite_name, composite_file in self.get_composite_files( dataset = dataset ).iteritems():
            fn = composite_name
            log.debug( "Velvet log info  %s %s %s" % ('JJ generate_primary_file',fn,composite_file))
            opt_text = ''
            if composite_file.optional:
                opt_text = ' (optional)'
            if composite_file.get('description'):
                rval.append( '<li><a href="%s" type="text/plain">%s (%s)</a>%s</li>' % ( fn, fn, composite_file.get('description'), opt_text ) )
            else:
                rval.append( '<li><a href="%s" type="text/plain">%s</a>%s</li>' % ( fn, fn, opt_text ) )
        rval.append( '</ul></body></html>' )
        return "\n".join( rval )

    def regenerate_primary_file(self,dataset):
        """
        cannot do this until we are setting metadata 
        """
        flist = os.listdir(dataset.extra_files_path)
        rval = ['<html><head><title>CuffDiff Output</title></head>']
        rval.append('<body>')
        rval.append('<p/>CuffDiff Outputs:<p/><ul>')
        for i,fname in enumerate(flist):
            sfname = os.path.split(fname)[-1]
            rval.append( '<li><a href="%s" type="text/html">%s</a>' % ( sfname, sfname ) )
        rval.append( '</ul></body></html>' )
        f = file(dataset.file_name,'w')
        f.write("\n".join( rval ))
        f.write('\n')
        f.close()

    def set_meta( self, dataset, **kwd ):
        Html.set_meta( self, dataset, **kwd )
        self.regenerate_primary_file(dataset)

    def sniff( self, filename ):
        return False

class CuffDataDB( Binary ):
    file_ext = 'cuffdatadb'
    is_binary = True
    allow_datatype_change = False
    MetadataElement( name="sample_names", default=[], desc="Sample names", readonly=True, visible=True, optional=True, no_value=[] )
    MetadataElement( name="replicate_names", default=[], desc="Replicate names", readonly=True, visible=True, optional=True, no_value=[] )
    MetadataElement( name="gene_ids", default=[], desc="Gene Ids", readonly=True, visible=True, optional=True, no_value=[] )

    def __init__( self, **kwd ):
        Binary.__init__( self, **kwd )
        log.info('Creating cummeRbund CuffDataDB')

    def set_meta( self, dataset, **kwd ):
        def get_contents(fname):
            contents = ''
            with open(fname,'r') as fh:
                contents = fh.read()
            return contents
        if not dataset.has_data():
            return
        try:
            ## Create a tmpdir
            ## create an Rscript to write out info about the CuffData, e.g. samples replicates gene_ids
            ## define file names to use as sinks for each type of data
            tmp_dir = tempfile.mkdtemp()
            if not os.path.isdir(tmp_dir):
                os.makedirs(tmp_dir)
            rscript = tempfile.NamedTemporaryFile( dir=tmp_dir,suffix='.r' ).name
            rscript_fh = open( rscript, 'wb' )
            rscript_fh.write('library(cummeRbund)\n')
            rscript_fh.write('cuff<-readCufflinks(dir = "", dbFile = "%s", rebuild = F)\n' % (dataset.file_name))
            rscript_fh.write('sink("%s")\n' % ("out.blurb"))
            rscript_fh.write('print(cuff)\n')
            rscript_fh.write('sink()\n')
            rscript_fh.write('sink("%s")\n' % ("out.samples"))
            rscript_fh.write('cat(samples(cuff)[[2]],sep=",")\n')
            rscript_fh.write('sink()\n')
            rscript_fh.write('sink("%s")\n' % ("out.replicates"))
            rscript_fh.write('cat(replicates(cuff)[[4]],sep=",")\n')
            rscript_fh.write('sink()\n')
            rscript_fh.write('sink("%s")\n' % ("out.gene_ids"))
            rscript_fh.write('cat(annotation(genes(cuff))[[1]],sep=",")\n')
            rscript_fh.write('sink()\n')
            rscript_fh.close()
            cmd = ( "Rscript --vanilla %s" % rscript )
            tmp_stderr_name = tempfile.NamedTemporaryFile( dir=tmp_dir,suffix='.err' ).name
            tmp_stderr = open( tmp_stderr_name, 'wb' )
            proc = Popen( args=cmd, shell=True, cwd=tmp_dir, stderr=tmp_stderr.fileno() )
            returncode = proc.wait()
            tmp_stderr.close()
            flist = os.listdir(tmp_dir)
            for i,fname in enumerate(flist):
                sfname = os.path.split(fname)[-1]
                if sfname == 'out.blurb':
                    dataset.blurb = get_contents(os.path.join(tmp_dir,fname))
                elif sfname == 'out.samples':
                    dataset.metadata.sample_names = get_contents(os.path.join(tmp_dir,fname)).split(',')
                elif sfname == 'out.replicates':
                    dataset.metadata.replicate_names = get_contents(os.path.join(tmp_dir,fname)).split(',')
                elif sfname == 'out.gene_ids':
                    dataset.metadata.gene_ids = get_contents(os.path.join(tmp_dir,fname)).split(',')
        except Exception, e:
            log.error('Error setting cummeRbund CuffDataDB metadata : %s' % str(e))

