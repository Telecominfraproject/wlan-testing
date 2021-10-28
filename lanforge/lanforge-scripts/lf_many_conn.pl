#!/usr/bin/perl -w

# This program is used to stress test the LANforge system, and may be used as
# an example for others who wish to automate LANforge tests.

# The purpose of this script is to create as many TCP (or UDP) connections
# as possible during a given amount of time.  If you tell later scripts not
# to initialize things to defaults, then you can run multiple copies of this
# script at once by changing the starting CX number.  This script not only
# starts and stops connections, but also verifys that both ends of the connection
# have received data before tearing the connection down.  (Errors will be printed
# to the console if the connection does not start in 15 seconds.)

# Written by Candela Technologies Inc.
#  Udated by:
#
#

use strict;
use warnings;
use diagnostics;

# Un-buffer output
$| = 1;

# use lib prepends to @INC, so put lower priority first
# This is before run-time, so cannot condition this with normal 'if' logic.
use lib '/home/lanforge/scripts';
use lib "./";

use LANforge::Endpoint;
use LANforge::Port;
use LANforge::Utils;
use Net::Telnet ();
use Getopt::Long;

my $lfmgr_host = "localhost";
my $lfmgr_port = 4001;

my $shelf_num = 1;

# Specify 'card' numbers for this configuration.
my $lanf1 = 7;
my $lanf2 = 5;

# Script assumes that we are using one port on each machine for data transmission...specifically
# port 1.

my $test_mgr = "conn-mgr";


# Run for XX seconds before tearing down and bringing up the next set..
my $run_for_time = 1000;
my $report_timer = 20000; # XX/1000 seconds

# Default values for ye ole cmd-line args.
my $proto = "tcp";  # tcp, udp, or both
my $to_do_at_a_time = 3000; # Do XX cross-connects at a time.  Don't make this too big...
my $quiet = "yes";
my $start_cx_num = 0;
my $init_to_dflts = "yes";
# Port pairs.  These are the ports that should be talking to each other.
# Ie, the first item lf1_ports talks to the third column in lf2_ports.
# Syntax is: port_num ip_addr ip_mask ip_gateway(dlft_router)
my $lf1_port = "2 172.16.1.200 255.255.255.0 172.16.1.1";
my $lf2_port = "2 172.16.1.220 255.255.255.0 172.16.1.1";


my $min_rate_a = 1000;
my $max_rate_a = 1000;
my $min_rate_b = 128000;
my $max_rate_b = 3000000;
my $wsize_min_a = 4000; # Write size
my $wsize_max_a = 4000; # Write size
my $wsize_min_b = 24000; # Write size
my $wsize_max_b = 24000; # Write size
my $rcvb_a = 64000;
my $rcvb_b = 16000;
my $txb_a = 16000;
my $txb_b = 64000;

my $do_bulk_removes = 0;
my $start_all_cx_at_once = 1;
my $do_cx_too = 1; # Should probably be 1 most of the time...
my $do_run_cxs = 1; #Should usually be 1
my $fail_msg = "";
my $manual_check = 0;

#my $cmd_log_name = "lf_conn_cmds.txt";
#open(CMD_LOG, ">$cmd_log_name") or die("Can't open $cmd_log_name for writing...\n");
#print "History of all commands can be found in $cmd_log_name\n";

########################################################################
# Nothing to configure below here, most likely.
########################################################################

my $usage = "$0  [--lf1_port {\"port_num ip mask gateway\"}]
                 [--lf2_port {\"port_num ip mask gateway\"}]
                 [--protocol {tcp | udp}]
                 [--start_cx_num {num}]
                 [--quiet {yes | no}]
                 [--num_cxs {num}]
                 [--init_to_dflts {yes | no}]

Example:
 $0 --lf1_port \"1 172.22.22.2 255.255.255.0 172.22.22.1\" --lf2_port \"1 172.22.22.3 255.255.255.0 172.22.22.1\" --init_to_dflts yes\n";

GetOptions 
(
        'protocol|p=s'          => \$proto,
        'start_cx_num|s=i'      => \$start_cx_num,
        'quiet|q=s'             => \$quiet,
        'num_cxs|n=i'           => \$to_do_at_a_time,
        'init_ports|i=s'        => \$init_to_dflts,
        'lf1_port|a=s'          => \$lf1_port,
        'lf2_port|b=s'          => \$lf2_port,
        'init_to_dflts|d=s'     => \$init_to_dflts,
) || die("$usage");


my @endpoint_names = (); #will be added to as they are created
my @cx_names = ();

# Open connection to the LANforge server.

my $t = new Net::Telnet(Prompt => '/default\@btbits\>\>/');


$t->open(Host    => $lfmgr_host,
	 Port    => $lfmgr_port,
	 Timeout => 10);

$t->waitfor("/btbits\>\>/");

# Configure our utils.
my $utils = new LANforge::Utils();
$utils->telnet($t);         # Set our telnet object.
$utils->cli_send_silent(0); # Do show input to CLI
$utils->cli_rcv_silent(1);  # Repress output from CLI ??

if ($init_to_dflts eq "yes") {
  initToDefaults();

  # Now, add back the test manager we will be using
  $utils->doCmd("add_tm $test_mgr");
  $utils->doCmd("tm_register $test_mgr default");  #Add default user
  $utils->doCmd("tm_register $test_mgr default_gui");  #Add default GUI user

  setUpPorts();
}

# $utils->doCmd("log_level 63");


# Create the connections we will be manipulating.
my $i = 0;
my $ep = $start_cx_num * 2;

my $cmd = "";
my $cx = $start_cx_num;


my $burst_a = "NO";
if ($min_rate_a != $max_rate_a) {
  $burst_a = "YES";
}
my $burst_b = "NO";
if ($min_rate_b != $max_rate_b) {
  $burst_b = "YES";
}

my $szrnd_a = "NO";
if ($wsize_min_a != $wsize_max_a) {
  $szrnd_a = "YES";
}

my $szrnd_b = "NO";
if ($wsize_min_b != $wsize_max_b) {
  $szrnd_b = "YES";
}


for ($i = 0; $i<$to_do_at_a_time; $i++) {
  my $pattern = "INCREASING";
  my $epnum = $i;
  my $ep1 = "l3e-${ep}-TX";

  $ep++;
  my $ep2 = "l3e-${ep}-RX";
  $ep++;

  my ($pn, $ip, $msk, $gw) = split(/\s+/, $lf1_port);

  @endpoint_names = (@endpoint_names, $ep1, $ep2);

  $cmd = "add_endp $ep1 $shelf_num $lanf1 $pn lf_$proto -1 $burst_a $min_rate_a $max_rate_a $szrnd_a $wsize_min_a $wsize_max_a $pattern NO";
  $utils->doCmd($cmd);

  $cmd = "set_endp_details $ep1 $rcvb_a $txb_a";
  $utils->doCmd($cmd);


  # Don't verify these, for speed reasons (and they should always work unless something
  # is mis-configured.
  #my $endp1 = new LANforge::Endpoint();
  #$utils->updateEndpoint($endp1, $ep1);
  #verifyEndpointAttributes($endp1, $ep1, $shelf_num, $lf1, $lf1_ports[$j], $cx_types[$i], -1, $burst,
  #                         $min_rate, $max_rate, $szrnd, $min_pkt_szs[$i], $max_pkt_szs[$i], $pattern,
  #                         "NO"); # last is use_checksum

  ($pn, $ip, $msk, $gw) = split(/\s+/, $lf2_port);
  $cmd = "add_endp $ep2 $shelf_num $lanf2 $pn lf_$proto -1 $burst_b $min_rate_b $max_rate_b $szrnd_b $wsize_min_b $wsize_max_b $pattern NO";

  $utils->doCmd($cmd);

  $cmd = "set_endp_details $ep2 $rcvb_b $txb_b";
  $utils->doCmd($cmd);

  # Now, add the cross-connects
  my $cx_name = "cx-${cx}";
  $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
  $utils->doCmd($cmd);
  $utils->doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");

  $cx++;

  @cx_names = (@cx_names, $cx_name);
}#addCrossConnects


# Now, bring up and down connections

my $tot_cx_started = 0;
my $begin_time = time();

while (1) {
  my $stime = time();

  if ($start_all_cx_at_once) {
    my $nm = $cx_names[$i];
    $cmd = "set_cx_state $test_mgr ALL RUNNING";
    $utils->doCmd($cmd);
  }
  else {
    for ($i = 0; $i<@cx_names; $i++) {
      my $nm = $cx_names[$i];
      $cmd = "set_cx_state $test_mgr $nm RUNNING";
      $utils->doCmd($cmd);
    }
}

  # Make sure they all started, and wait untill both sides have received
  # a packet or two.
  my $slp = 0;
  for ($i = 0; $i<@endpoint_names; $i++) {
    my $endp1 = new LANforge::Endpoint();
    my $en = $endpoint_names[$i];
    $utils->updateEndpoint($endp1, $en);
    while ($endp1->rx_pkts() <= 0) {
      if ($slp > 14) {
	# Things are not working right, it should never take this long
	print "WARNING:  Endpoint $en is not receiving packets after $slp seconds.\n";
	last;
      }
      $slp++;
      sleep(1);
      $utils->updateEndpoint($endp1, $en);
    }
  }

  # Stop cxs.
  for ($i = 0; $i<@cx_names; $i++) {
    my $nm = $cx_names[$i];
    $cmd = "set_cx_state $test_mgr $nm STOPPED";
    $utils->doCmd($cmd);
  }

  my $elapsed = time() - $stime;
  my $tot_elapsed = time() - $begin_time;

  $i = @cx_names;
  $tot_cx_started += $i;
  print "\nStarted and stopped $i connections this round in $elapsed seconds.\n";
  print "Started and stopped a total of $tot_cx_started in $tot_elapsed seconds.\n\n";

}

exit(0);


sub initToDefaults {
  # Clean up database if stuff exists

  $utils->doCmd("rm_cx $test_mgr all");
  $utils->doCmd("rm_endp YES_ALL");
  $utils->doCmd("rm_test_mgr $test_mgr");

  # initPortsToDefault();
}#initToDefaults


sub initPortsToDefault {
  # Set all ports we are messing with to known state.
  my $i = 0;
  my ($pn, $ip, $msk, $gw) = split(/\s+/, $lf1_port);
  $utils->doCmd("set_port $shelf_num $lanf1 $pn 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");

  ($pn, $ip, $msk, $gw) = split(/\s+/, $lf2_port);
  $utils->doCmd("set_port $shelf_num $lanf2 $pn 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
}

sub testFailed {
  my $msg = shift;
  my $should_fail = shift;

  if (defined($should_fail) && ($should_fail eq "YES")) {
    print "\nGOOD: SUB-TEST FAILED correctly: $msg\n";
    $fail_msg .= "GOOD (should fail): $msg";
  }
  else {
    print "\nSUB-TEST FAILED: $msg\n";
    $fail_msg .= $msg;

    if ($manual_check) {
      #$utils->doCmd("log_level 7");
      print "Press enter to continue with test: ";
      <STDIN>;
    }
    else {
      die("FATAL ERROR: $fail_msg\n");
    }
  }
}#testFailed

sub setUpPorts {
  # Set all ports we are messing with to known state.
  my $i = 0;

  my ($pn, $ip, $msk, $gw) = split(/\s+/, $lf1_port);
  my $cmd = "set_port $shelf_num $lanf1 $pn $ip $msk $gw NA NA NA";
  $utils->doCmd($cmd);
  my $p1 = new LANforge::Port();
  # Tell the port what it is so it decodes the right one..
  $utils->updatePort($p1, $shelf_num, $lanf1, $pn);
  # Make sure the values we attempted to set actually worked.
  verifyPortAttributes($p1, $shelf_num, $lanf1, $pn, $ip, $msk, $gw);


  ($pn, $ip, $msk, $gw) = split(/\s+/, $lf2_port);
  $cmd = "set_port $shelf_num $lanf2 $pn $ip $msk $gw NA NA NA";
  $utils->doCmd($cmd);
  my $p2 = new LANforge::Port();
  ($pn, $ip, $msk, $gw) = split(/\s+/, $lf2_port);
  # Tell the port what it is so it decodes the right one..
  $utils->updatePort($p2, $shelf_num, $lanf2, $pn);

  verifyPortAttributes($p2, $shelf_num, $lanf2, $pn, $ip, $msk, $gw);

}#setUpPorts


sub verifyPortAttributes {
  my $port = shift;
  my $sn = shift;
  my $cn = shift;
  my $pn = shift;
  my $ip = shift;
  my $msk = shift;
  my $gw = shift;

  my $_sn = $port->shelf_id();
  my $_cn = $port->card_id();
  my $_pn = $port->port_id();
  my $_ipa = $port->ip_addr();

  my $p = $port->toStringBrief();

  $_sn eq $sn or testFailed("$p: Shelf id: $_sn does not match: $sn\n");
  $_cn eq $cn or testFailed("$p: Card id: $_cn does not match: $cn\n");
  $_pn eq $pn or testFailed("$p: Port id: $_pn does not match: $pn\n");
  $_ipa eq $ip or testFailed("$p: IP Address: $_ipa does not match: $ip\n");
  $port->ip_mask() eq $msk or testFailed("$p: IP Mask: " . $port->ip_mask() . " does not match: $msk\n");
  $port->ip_gw() eq $gw or testFailed("$p: IP Gateway: " . $port->ip_gw() . " does not match: $gw\n");

  print "$p verified as correct!\n";
}#verifyPortAttributes


sub verifyEndpointAttributes {
  my $endp = shift;
  my $name = shift;
  my $sn = shift;
  my $cn = shift;
  my $pn = shift;
  my $type = shift;
  my $ip_port = shift;
  my $bursty = shift;
  my $min_rate = shift;
  my $max_rate = shift;
  my $szrnd = shift;
  my $min_pkt_sz = shift;
  my $max_pkt_sz = shift;
  my $pattern = shift;
  my $using_csum = shift;
  my $should_fail = shift;

  my $_sn = $endp->shelf_id();
  my $_cn = $endp->card_id();
  my $_pn = $endp->port_id();

  my $p = $endp->toStringBrief();

  $_sn eq $sn or testFailed("$p: Shelf id: $_sn does not match: $sn\n", $should_fail);
  $_cn eq $cn or testFailed("$p: Card id: $_cn does not match: $cn\n", $should_fail);
  $_pn eq $pn or testFailed("$p: Port id: $_pn does not match: $pn\n", $should_fail);
  $endp->isOfType($type) or testFailed("$p: Type: " . $endp->ep_type() . " does not match: $type\n", $should_fail);
  if ($ip_port ne -1) {
    $endp->ip_port() eq $ip_port or testFailed("$p: IP-Port: " . $endp->ip_port() .
					       " does not match: $ip_port\n", $should_fail);
  }
  $endp->getBursty() eq $bursty or testFailed("$p: Bursty: " . $endp->getBursty() .
					      " does not match: $bursty\n", $should_fail);

  $endp->min_tx_rate() eq $min_rate or testFailed("$p: Min-Tx-Rate: " . $endp->min_tx_rate() .
						  " does not match: $min_rate\n", $should_fail);
  $endp->max_tx_rate() eq $max_rate or testFailed("$p: Max-Tx-Rate: " . $endp->max_tx_rate() .
						  " does not match: $max_rate\n", $should_fail);

  if ($endp->isCustom()) {
    ($endp->size_random() eq "NO") or testFailed("$p: Size-Random: " . $endp->size_random() .
						 " but we are CUSTOM!!\n", $should_fail);
  }
  else {
    $endp->size_random() eq $szrnd or testFailed("$p: Size-Random: " . $endp->size_random() .
						 " does not match: $szrnd\n", $should_fail);
  }

  if (! $endp->isCustom()) {
    $endp->min_pkt_size() eq $min_pkt_sz or testFailed("$p: Min-Packet-Size: " . $endp->min_pkt_size() .
						       " does not match: $min_pkt_sz\n", $should_fail);
    $endp->max_pkt_size() eq $max_pkt_sz or testFailed("$p: Max-Packet-Size: " . $endp->max_pkt_size() .
						       " does not match: $max_pkt_sz\n", $should_fail);
  }
  $endp->pattern() eq $pattern or testFailed("$p: Pattern: " . $endp->pattern() .
					     " does not match: $pattern\n", $should_fail);
  $endp->checksum() eq $using_csum or testFailed("$p: Using-Checksum: " . $endp->checksum() .
						 " does not match: $using_csum\n", $should_fail);

}#verifyEndpointAttributes


sub genRandomHex {
  my $bytes = shift;

  my @tbl = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f");
  my $i;
  my $pld = "";
  for ($i = 0; $i<$bytes; $i++) {
    $pld .= $tbl[(rand() * 1000.0) % 16] . $tbl[(rand() * 1000.0) % 16];  #Generate some hex the hard way!
    if ($i != ($bytes - 1)) {
      $pld .= " ";
    }
  }

  return $pld;
}#genRandomHex
