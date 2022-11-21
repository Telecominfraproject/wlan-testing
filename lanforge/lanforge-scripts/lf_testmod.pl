#!/usr/bin/perl -w

# This program is used to load GUI tests (TR-398, Capacity, etc) from a file
# and configure it in the LANforge server.  See gui/README.txt
# (C) 2020 Candela Technologies Inc.
#
#

use strict;
use warnings;
use diagnostics;
use Carp;
$SIG{ __DIE__  } = sub { Carp::confess( @_ ) };
$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };

# Un-buffer output
$| = 1;

# use lib prepends to @INC, so put lower priority first
# This is before run-time, so cannot condition this with normal 'if' logic.
use lib '/home/lanforge/scripts';
use lib "../";
use lib "./";

use LANforge::Endpoint;
use LANforge::Port;
use LANforge::Utils;
use Net::Telnet ();
use Getopt::Long;

our $NA        = 'NA';
our $NL        = "\n";

# Default values for ye ole cmd-line args.
our $quiet            = "yes";
our $test_type        = "Plugin-Settings";
our $test_name        = "";
our $file_name        = "";
our $action           = "show";
our $lfmgr_host       = "localhost";
our $lfmgr_port       = 4001;

########################################################################
# Nothing to configure below here, most likely.
########################################################################

our $usage = <<"__EndOfUsage__";
$0 [ --action {
     show | set
  } ]
  [--file         {data file name}]
  [--test_name    {test name or ALL}]
  [--test_type    {Plugin-Settings or other type or ALL}]
  [--mgr          {host-name | IP}]
  [--mgr_port     {ip port}]
  [--quiet        { yes | no }]
  [--log_cli      {1|filename}]

Example:
 $0 --action set --test_name AP-Auto-ap-auto-32-64-dual --file test_configs/AP-Auto-ap-auto-32-64-dual.txt
__EndOfUsage__

my $i = 0;
my $cmd;

my $log_cli = "unset"; # use ENV{LOG_CLI} elsewhere
my $show_help = 0;

if (@ARGV < 2) {
   print $usage;
   exit 0;
}

our $debug = 0;

GetOptions
(
   'action|a=s'         => \$::action,
   'file=s'             => \$::file_name,
   'test_name=s'        => \$::test_name,
   'test_type=s'        => \$::test_type,
   'debug|d'            => \$::debug,
   'help|h'             => \$show_help,
   'log_cli=s{0,1}'     => \$log_cli,
   'manager|mgr|m=s'    => \$::lfmgr_host,
   'lfmgr_port|mgr_port|port|p=i' => \$::lfmgr_port,
   'quiet|q=s'          => \$::quiet,

) || die("$::usage");

if ($show_help) {
   print $usage;
   exit 0;
}

use Data::Dumper;

if ($::debug) {
  $ENV{DEBUG} = 1 if (!(defined $ENV{DEBUG}));
}

if ($::quiet eq "0") {
  $::quiet = "no";
}
elsif ($::quiet eq "1") {
  $::quiet = "yes";
}

if (defined $log_cli) {
  if ($log_cli ne "unset") {
    # here is how we reset the variable if it was used as a flag
    if ($log_cli eq "") {
      $ENV{'LOG_CLI'} = 1;
    }
    else {
      $ENV{'LOG_CLI'} = $log_cli;
    }
  }
}

our @valid_actions = qw(show set);

if (! (grep {$_ eq $::action} @::valid_actions )) {
  die("Invalid action: $::action\n$::usage\n");
}
if ($::quiet eq "1" ) {
   $::quiet = "yes";
}

# Open connection to the LANforge server.
our $utils = new LANforge::Utils();
$::utils->connect($lfmgr_host, $lfmgr_port);


if ($::action eq "show") {
   $cmd = "show_text_blob $test_type $test_name";
   my $txt = $::utils->doCmd($cmd);
   my @r = split(/\n/, $txt);
   my $first = $r[0];
   chomp($first);
   if ($first =~ /.*::(.*)/) {
      print "$1\n";
   }
   my $i;
   for ($i = 1; $i<@r; $i++) {
      my $ln = $r[$i];
      chomp($ln);
      if ($ln =~ /\s*>>RSLT.*/) {
         # ignore
      }
      elsif ($ln =~ /\s*default\@btbits.*/) {
         # ignore
      }
      else {
         print "$ln\n";
      }
   }
}
elsif ($::action eq "set") {
   if ($file_name eq "") {
      print("ERROR:  Must specify file name when doing the 'set' action\n");
      exit(1);
   }

   my @cmds = `cat $file_name`;
   if (@cmds == 0) {
      print("ERROR:  Could not read any lines from the file: $file_name\n");
      exit(2);
   }

   # First clean out any old text blob.
   $cmd = "rm_text_blob $test_type $test_name";
   $::utils->doCmd($cmd);

   # And add the new blob
   for ($i = 0; $i<@cmds; $i++) {
      my $ln = $cmds[$i];
      chomp($ln);

      # Skip blank lines
      if ($ln eq "") {
         next;
      }

      $cmd = "add_text_blob '$test_type' '$test_name' $ln";
      print("$cmd\n");
      if (($i % 25) != 0) {
         $::utils->doCmd($cmd, 1);  # send and do not wait for result
      }
      else {
         $::utils->doCmd($cmd);  # send and wait for result
      }
   }

   # Wait until we complete processing of all cmds.
   $cmd = "gossip __gossip_test__";
   $::utils->doCmd($cmd, 0, "/__gossip_test__/");
}
else {
  die("Unknown action: $::action\n$::usage\n");
}

exit(0);

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
