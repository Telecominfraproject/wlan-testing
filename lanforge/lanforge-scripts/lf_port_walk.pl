#!/usr/bin/perl

# This program is used to stress test the LANforge system, and may be used as
# an example for others who wish to automate LANforge tests.

# The purpose of this script is to create 10 (or more) TCP and/or UDP connections on
# specified ports.  The connections will run for a short period of time, and
# then 10 more will be created on a new set of ports (the next 10).  It
# writes it's cmds to a log file so you can get an idea of what it's doing.
#
# This script should be useful for people who are testing firewalls and other
# types of systems that care about what ports the data is transmitted on...
#
# Written by Candela Technologies Inc.
#  Udated by:
#
#

# Un-buffer output
$| = 1;

use Net::Telnet ();
use Getopt::Long;

my $lfmgr_host = "localhost";
my $lfmgr_port = 4001;

my $shelf_num = 1;

# Specify 'card' numbers for this configuration.
my $lanf1 = 1;
my $lanf2 = 2;

# Script assumes that we are using one port on each machine for data transmission...specifically
# port 1.

my $test_mgr = "port-walker";


my $run_for_time = 20;  # Run for XX seconds before tearing down and bringing up the next set..
my $report_timer = 8000; # XX/1000 seconds

# Default values for ye ole cmd-line args.
my $proto = "both";  # tcp, udp, or both
my $start_port = 1; # Port to start with...
my $end_port   = 65535;  # port to end with
my $to_do_at_a_time = 20; # Do XX cross-connects at a time.  Don't make this too big,
                          # especially now...there is a buglet w/the GUI, especially...
my $do_bulk_removes = 1;
my $do_cx_too = 1; # Should probably be 1 most of the time...
my $do_run_cxs = 1; #Should usually be 1

my $cmd_log_name = "lf_port_walk_cmds.txt";
open(CMD_LOG, ">$cmd_log_name") or die("Can't open $cmd_log_name for writing...\n");
print "History of all commands can be found in $cmd_log_name\n";

########################################################################
# Nothing to configure below here, most likely.
########################################################################

my $usage = "$0 [--protocol={tcp | udp | both}] [--start_port={port}] [--end_port={port}]\n";

my $i = 0;

GetOptions 
(
	'protocol|p=s'		=> \$proto,
	'start_port|s=i'	=> \$start_port,
	'end_port|e=i'  	=> \$end_port,
) || die("$usage");


my @endpoint_names = (); #will be added to as they are created
my @cx_names = ();

# Open connection to the LANforge server.

my $t = new Net::Telnet(Prompt => '/default\@btbits\>\>/');


$t->open(Host    => $lfmgr_host,
	 Port    => $lfmgr_port,
	 Timeout => 10);

$t->waitfor("/btbits\>\>/");

my $dt = "";

# Lets create udp and tcp connections on all ports.  Some of these
# won't work, so we'll ignore them.

# get these numbers by doing something like:
# netstat -an | grep LISTEN
#  There may be more or less on your machine...it would be best to check with the
#  above cmd.
#
my @tcp_ignore_array = (
6010, # X
3999, 4002, 4001,  # LANforge
1024, # varies, rpc.statd often
111, # portmapper for NFS
22, #ssh
25, #smtp (email)
);

# Set up a hash for fast existence checking...
my %ignore_ports = ();
for ($i = 0; $i<@tcp_ignore_array; $i++) {
  my $prt = $tcp_ignore_array[$i];
  $ignore_ports->{$prt} = "$prt";
}

$dt = `date`;
chomp($dt);
print "\n\n*****  Starting loop at: $dt  *****\n\n";

# Remove any existing configuration information
initToDefaults();
  
print " ***Sleeping 3 seconds for ports to initialize to defaults...\n";
sleep(3);

#exit(0);

# Now, add back the test manager we will be using
doCmd("add_tm $test_mgr");
doCmd("tm_register $test_mgr default");  #Add default user
doCmd("tm_register $test_mgr default_gui");  #Add default GUI user

# Add some IP addresses to the ports
initIpAddresses();

print " ***Sleeping 3 seconds for ports to initialize to current values...\n";
sleep(3);


# Now, go build lots of endpoints, one for every tcp/udp port known to man and beast!
for ($i = $start_port; $i<$end_port; $i++) {

  # Do XX at once.
  my $j = 0;
  for ($j = 0; $j<$to_do_at_a_time; $j++) {

    my $ht = $ignore_ports->{$i};
    if ((defined($ht)) && (length($ht) > 0)) {
      # continue...it's in our ignore list
      # TODO: We could probably still do UDP, so we should really have separate
      #       ingore lists for the different protocols...
      print " *** Skipping port: $i\n";
      $i++;
      next;
    }

    # Syntax for adding an endpoint is:
    # add_endp [alias] [shelf] [card] [port] [type] [IP-port] [bursty] [min_rate] [max_rate]
    #          [pkt_sz_random] [min_pkt] [max_pkt] [pattern] [use_checksum]

    if (($proto eq "both") || ($proto eq "udp")) {
      # Set up 128Kbps full duplex UDP link, 1200 byte UDP payloads, on port $i
      print " *** Creating UDP endpoint on port $i\n";
      doCmd("add_endp udp-$i-TX $shelf_num $lanf1 1 lf_udp $i NO 512000 512000 NO 1200 1200 increasing NO");
      doCmd("add_endp udp-$i-RX $shelf_num $lanf2 1 lf_udp $i NO 512000 512000 NO 1200 1200 increasing NO");
      if ($do_cx_too) {
	doCmd("add_cx udp-$i $test_mgr udp-${i}-TX udp-${i}-RX");
	@cx_names = (@cx_names, "udp-$i");
      }

      @endpoint_names = (@endpoint_names, "udp-${i}-TX", "udp-${i}-RX");
    }

    if (($proto eq "both") || ($proto eq "tcp")) {
      # Set up 128Kbps full duplex TCP link, 1200 byte TCP payloads, on port $i
      print " *** Creating TCP endpoint on port $i\n";
      doCmd("add_endp tcp-$i-TX $shelf_num $lanf1 1 lf_tcp $i NO 512000 512000 NO 1200 1200 increasing NO");
      doCmd("add_endp tcp-$i-RX $shelf_num $lanf2 1 lf_tcp $i NO 512000 512000 NO 1200 1200 increasing NO");
      if ($do_cx_too) {
	doCmd("add_cx tcp-$i $test_mgr tcp-${i}-TX tcp-${i}-RX");
	@cx_names = (@cx_names, "tcp-$i");
      }

      @endpoint_names = (@endpoint_names, "tcp-${i}-TX", "tcp-${i}-RX");
    }

    $i++;
    if ($i >= $end_port) {
      last;
    }
  }
  
  # So, our CXs and endpoints are created...lets start them running.
  if ($do_run_cxs) {
    doCmd("set_cx_state $test_mgr all RUNNING");
  }

  # SLeep for a bit, because it takes connections, especially TCP a bit to get started
  # properly...and we want to give the user time to see if the expected behaviour is
  # really happening....

  print " ***Done starting endpoints...sleeping $run_for_time seconds.\n";
  sleep($run_for_time);

  if ($do_run_cxs) {
    doCmd("set_cx_state $test_mgr all STOPPED");
  }

  my $q = 0;
  if (! $do_bulk_removes) {
    for ($q = 0; $q<@cx_names; $q++) {
      # Delete the endpoints and cross-connects related to this test manager.
      doCmd("rm_cx $test_mgr $cx_names[$q]");
    }
    
    for ($q = 0; $q<@endpoint_names; $q++) {
      # Delete the endpoints and cross-connects related to this test manager.
      doCmd("rm_endp $endpoint_names[$q]");
    }
  }
  else {
    doCmd("rm_cx $test_mgr ALL");
    doCmd("rm_endp YES_ALL"); # Won't delete those attached to cross-connects still...
  }

  @endpoint_names = ();
  @cx_names = ();

}# for all ports


$dt = `date`;
chomp($dt);
print "Done at: $dt\n\n";
exit(0);


sub initToDefaults {
  # Clean up database if stuff exists

  doCmd("rm_cx $test_mgr all");
  doCmd("rm_endp YES_ALL");
  doCmd("rm_test_mgr $test_mgr");

  initPortsToDefault();
}#initToDefaults


sub initPortsToDefault {
  # Set all ports we are messing with to known state.
  my $i = 0;
  my $num_ports = 1;
  for ($i = 1; $i<=$num_ports; $i++) {
    doCmd("set_port $shelf_num $lanf1 $i 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
    doCmd("set_port $shelf_num $lanf2 $i 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
  }

}


sub initIpAddresses {
  # Set all ports we are messing with to known state.

  # Syntax for setting port info is:
  # set_port [shelf] [card] [port] [ip] [mask] [gateway] [cmd-flags] [cur-flags] [MAC]
  # NOTE:  Just use NA for the flags for now...not tested otherwise.

  doCmd("set_port $shelf_num $lanf1 1 172.25.7.2 255.255.255.0 172.25.7.1 NA NA NA");
  doCmd("set_port $shelf_num $lanf2 1 172.25.7.3 255.255.255.0 172.25.7.1 NA NA NA");
}

sub doCmd {
  my $cmd = shift;

  print CMD_LOG "$cmd\n";
  print ">>> $cmd\n";

  $t->print($cmd);
  my @rslt = $t->waitfor('/ \>\>RSLT:(.*)/');
  print "**************\n @rslt ................\n\n";
  #sleep(1);
}
