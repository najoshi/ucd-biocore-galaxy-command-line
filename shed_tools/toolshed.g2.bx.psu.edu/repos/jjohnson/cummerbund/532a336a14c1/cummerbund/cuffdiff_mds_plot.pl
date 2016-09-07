#!/usr/bin/perl -w

###############################################################
# cuffdiff_mds_plot.pl
# John Garbe
# Septmeber 2012
#
# Given a sample tracking file from cuffdiff2, convert it to 
# the proper format for loading into R and generating an MDS plot
#
################################################################

# check to make sure having correct files
my $usage = "usage: cuffdiff_mds_plot.pl [TABULAR.in] [TABULAR.out] [PLOT.png]\n";
die $usage unless @ARGV == 3;
 
#get the input arguments
my $inputFile = $ARGV[0];
my $outputFile = $ARGV[1];
my $plotFile = $ARGV[2];

#Open files
open (INPUT, "<", $inputFile) || die("Could not open file $inputFile \n");
open (OUTPUT, ">", $outputFile) || die("Could not open file $outputFile \n");
open (PLOT, ">", $plotFile) || die("Could not open file $plotFile \n");

# header looks like this:
# tracking_id condition replicate raw_frags internal_scaled_frags external_scaled_frags FPKM effective_length status
my $header = <INPUT>;

# read in the sample tracking file
while (<INPUT>) {
    chomp;
    @line = split /\t/;
    $tracking_id{$line[0]} = 1;
    $sample = $line[1] . "-" . $line[2];
    $fpkm{$sample}{$line[0]} = $line[6];
}
close(INPUT);

@sorted_tracking_id = sort( keys(%tracking_id));

# print out header
foreach $tracking_id (@sorted_tracking_id) {
    print OUTPUT "\t$tracking_id";
}
print OUTPUT "\n";

# print out data
foreach $sample (keys(%fpkm)) {
    print OUTPUT "$sample";
    
    foreach $tracking_id (@sorted_tracking_id) {
	print OUTPUT "\t$fpkm{$sample}{$tracking_id}";
    }

    print OUTPUT "\n";
}
close(OUTPUT);

#variables to store the name of the R script file
my $r_script = "cuffinks2mdf.r";

open(Rcmd,">", $r_script) or die "Cannot open $r_script \n\n";
print Rcmd "
  datat <- read.table(\"$outputFile\"); 
  cmd <- cmdscale(dist(datat)); 
  png(filename=\"$plotFile\"); 
  plot(cmd[,1], cmd[,2], type=\"n\", ann=FALSE); 
  text(cmd[,1], cmd[,2], labels = rownames(datat)); 
  title(main=\"Multidimensional Scaling Plot\"); 
  title(xlab= \"Dimension 1\"); 
  title(ylab= \"Dimension 2\"); 
  dev.off();
  #eof" . "\n";

close Rcmd;


system("R --no-restore --no-save --no-readline < $r_script > $r_script.out");
#close the input and output files
close(PLOT);

