#!/usr/bin/perl -w

# This program is used to stress test the LANforge system, and may be used as
# an example for others who wish to automate LANforge tests.

# Written by Candela Technologies Inc.
#  Updated by: greearb@candelatech.com
#
#

use strict;
use warnings;
use diagnostics;
use Carp;
$SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };
# Un-buffer output
$| = 1;

use Net::Telnet ();
use Getopt::Long;

my $lfmgr_host = "localhost";
my $lfmgr_port = 3990;

# Default values for ye ole cmd-line args.
my $port = "";
my $cmd = "";
my $ttype = ""; # Test type
my $tname = "lfgui-test";
my $scenario = "";
my $tconfig = "";  # test config
my $rpt_dest = "";
my $show_help = 0;
my $verbosity = -1;
my @modifiers_key = ();
my @modifiers_val = ();

########################################################################
# Nothing to configure below here, most likely.
########################################################################

my $usage = qq($0  [--manager { hostname or address of LANforge GUI machine } ]
                 [--port {port name} ] # cli-socket port default 3990
                                       # careful, your cli-socket might be 3390!
                 [--ttype {test instance type} ]
                    # likely types: "cv", "WiFi Capacity", "Port Bringup", "Port Reset"
                 [--scenario {scenario name} ]
                    #  Apply and build the scenario.
                 [--tname {test instance name} ]
                 [--tconfig {test configuration name, use defaults if not specified} ]
                 [--rpt_dest {Copy report to destination once it is complete} ]
                 [--cmd { command to send to the GUI } ]
                 [--verbosity { report verbosity 1 - 11 } ]
                 [--modifier "

Example:
 lf_gui_cmd.pl --manager localhost --port 3990 --ttype TR-398 --tname mytest --tconfig comxim --rpt_dest /var/www/html/lf_reports
 lf_gui_cmd.pl --manager localhost --port 3990 --cmd \"help\"
 lf_gui_cmd.pl --manager localhost --port 3990 --scenario 64sta
);

if (@ARGV < 2) {
   print "$usage\n";
   exit 0;
}

GetOptions (
   'help|h'                => \$show_help,
   'manager|mgr|m=s'       => \$lfmgr_host,
   'modifier_key=s'        => \@modifiers_key,
   'modifier_val=s'        => \@modifiers_val,
   'ttype=s'               => \$ttype,
   'tname=s'               => \$tname,
   'scenario=s'            => \$scenario,
   'tconfig=s'             => \$tconfig,
   'rpt_dest=s'            => \$rpt_dest,
   'port=s'                => \$port,
   'cmd|c=s'               => \$cmd,
    'verbosity|v=i'         => \$verbosity,
) || die("$usage");

if ($show_help) {
   print $usage;
   exit 0;
}

my $lnk = @modifiers_key;
my $lnv = @modifiers_val;
if ($lnk != $lnv) {
   print("ERROR:  You must specify the same amount of modifers-key and modifiers-val entries.\n");
   exit(3);
}

if ((defined $port) && ($port > 0)) {
  $lfmgr_port = $port;
}

# Open connection to the LANforge server.
my $t = new Net::Telnet(Prompt => '/lfgui\# /',
         Timeout => 20);

$t->open( Host    => $lfmgr_host,
          Port    => $lfmgr_port,
          Timeout => 10);

$t->waitfor("/lfgui\# /");

if ($cmd ne "") {
  print doCmd("$cmd");
}

if ($scenario ne "") {
   print doCmd("cv apply '$scenario'");
   print doCmd("cv build");
   sleep(3);

   while (1) {
     my $rslt = doCmd("cv is_built");
     print "Result-built -:$rslt:-\n";
     if ($rslt =~ /NO/) {
        sleep(3);
     }
     else {
        last;
     }
  }
}

if ($ttype ne "") {
  # Try several times in case system is currently busy cleaning up or similar.
  my $i;
  my $rslt;
  for ($i = 0; $i<60; $i++) {
    $rslt = doCmd("cv create '$ttype' '$tname'");
    print $rslt;
    if ($rslt =~ /BUSY/) {
       sleep(1);
    }
    else {
       last;
    }
  }
  if ($tconfig ne "") {
    print doCmd("cv load '$tname' '$tconfig'");
  }
    if ($verbosity >= 1) {
        print doCmd("cv set '$tname' 'VERBOSITY' '$verbosity'");
    }
  print doCmd("cv click '$tname' 'Auto Save Report'");

  for ($i = 0; $i<@modifiers_key; $i++) {
     my $k = $modifiers_key[$i];
     my $v = $modifiers_val[$i];
     print doCmd("cv set '$tname' '$k' '$v'");
  }

  $rslt = doCmd("cv click '$tname' 'Start'");
  print $rslt;
  if ($rslt =~ /Could not find instance/) {
     exit(1);
  }

  while (1) {
    my $rslt = doCmd("cv get '$tname' 'Report Location:'");
    #print "Result-:$rslt:-\n";
    if ($rslt =~ /^\s*Report Location:::(.*)/) {
      my $loc = $1;
      if ($loc eq "") {
        # Wait longer
        sleep(3);
      }
      else {
        # Copy some place it can be seen easily?
        print("LANforge GUI test complete, rpt-dest: $rpt_dest  location: $loc\n");
        if ($rpt_dest ne "") {
          if ($lfmgr_host eq "localhost" || $lfmgr_host eq "127.0.0.1") {
            # Must be on the local system
            my $cp = "cp -ar $loc $rpt_dest";
            print "Copy test results: $cp\n";
            system($cp);
          }
          else {
            # Must be on remote system, try scp to get it.
            my $cp = "scp -r lanforge\@$lfmgr_host:$loc $rpt_dest";
            print "Secure Copy test results: $cp\n";
            system($cp);
          }
        }
        last;
      }
    }
    else {
      sleep(3);
    }
  }

  # Clean up our instance.  This can take a while.
  print doCmd("cv delete '$tname'");
  while (1) {
     my $rslt = doCmd("cv exists '$tname'");
     print "Result-exists -:$rslt:-\n";
     if ($rslt =~ /YES/) {
        sleep(3);
     }
     else {
        last;
     }
  }

  # Wait a bit more, CV will likey be rebuilt now.
  sleep(5);

  while (1) {
     my $rslt = doCmd("cv is_built");
     print "Result-built -:$rslt:-\n";
     if ($rslt =~ /NO/) {
        sleep(3);
     }
     else {
        print("Chamber-View is (re)built, exiting.\n");
        last;
     }
  }
}

exit(0);

sub doCmd {
  my $cmd = shift;

  print ">>>Sending:$cmd\n";

  $t->print($cmd);
  my @rslt = $t->waitfor('/lfgui\#/');
  if ($rslt[@rslt-1] eq "lfgui\#") {
    $rslt[@rslt-1] = "";
  }
  return join("\n", @rslt);
}

