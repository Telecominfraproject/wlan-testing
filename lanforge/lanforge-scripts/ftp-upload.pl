#!/usr/bin/perl -w

## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
##
##    Use this script to collect and upload station data
##    to an FTP host.
##
## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
use strict;
use warnings;
use Carp;
use Getopt::Long;
use Socket;
use Cwd;
use Net::FTP;
$SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
$| = 1;

## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
our $def_user     = 'anonymous';
our $def_pass     = 'anonymous';
our $def_srcdir   = Cwd::getcwd();
our $def_destdir  = '/WIN7_LanForge_Data/';
our $def_ftphost  = "192.168.1.222";
our @file_list    = ();
our $verbose      = 0;
our $debug        = 0;
our $username     = $def_user;
our $password     = $def_pass;
our $ftp_host     = $def_ftphost;
our $srcdir       = $def_srcdir;
our $destdir      = $def_destdir;
## ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
our $usage = "\n$0:
  --user    username       [$def_user]
  --passwd  password       [$def_pass]
  --srcdir  sourcedir      [$def_srcdir]
  --host    host           [$def_ftphost]
  --destdir destdir        [$def_destdir]
  --verbose=1              [$verbose]
  --debug=1                [$debug]
  -- file1 file2 ... fileN # use -- to start a list of files or globs on cmdline
";

GetOptions (
   'user|u=s'        => \$::username,
   'passwd|p=s'      => \$::password,
   'host|h=s'        => \$::ftp_host,
   'srcdir|s=s'      => \$::srcdir,
   'destdir|t=s'     => \$::destdir,
   'verbose|v=n'     => \$::verbose,
   'debug|d=n'       => \$::debug
) || die($usage);

die "Cannot open $srcdir " if ( ! -e $srcdir );

if (@ARGV > 0) {
   # we were passed -- file1 file2 ... fileN on commandline
   print "Checking files listed on command line...\n" if ($verbose);
   for my $filename (@ARGV) {
      if ($filename =~ /(\*|\?|\{\n)/) {
         my @expanded  = glob("$srcdir/$filename");
         for my $filename2 (@expanded) {
            if ( -e $filename2 ) {
               push(@file_list, $filename2);
            }
            else {
               print STDERR "File $filename2 not found\n";
            }
         }
      }
      else {
         if ( -e "$srcdir/$filename" ) {
            push(@file_list, "$srcdir/$filename");
         }
         else {
            print STDERR "File $srcdir/$filename not found\n";
         }
      }
   }
}
else {
   # we were just given a directory
   print "Looking for 'sta*.csv' files in $srcdir...\n" if ($verbose);
   @file_list  = glob("$srcdir/sta*.csv");
}

die "No CSV files present in $srcdir" if (@file_list < 1);
my $ftp_server = Net::FTP->new($ftp_host,
                              Debug=>$debug,
                              Timeout=>15,
                              Port=>21,
                              Passive=>0)
               or die "Can't open $ftp_host\n";

$ftp_server->login($username, $password)        or die "Can't log $username in\n";
$ftp_server->cwd($destdir)                      or die "Unable to cd to $destdir\n";

for my $filename (@file_list) {
   print "uploading $filename\n" if ($verbose);
   $ftp_server->put($filename)                  or die "Unable to upload $filename\n";
}
##
## eof
##
