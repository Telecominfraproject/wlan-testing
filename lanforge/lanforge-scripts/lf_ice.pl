#!/usr/bin/perl -w

# This program is used to stress test the LANforge system, and may be used as
# an example for others who wish to automate LANforge tests.

# Written by Candela Technologies Inc.
#  Creates a WanLink with 128 WanPaths for performance testing.

use strict;
use warnings;
use diagnostics;
use Carp;
$SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };

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
my $ice_card = 1;

# The ICE ports, on ice_card
my $ice1 = 1;
my $ice2 = 2;

my $test_mgr = "vanilla-ice"; # Couldn't resist!

my $report_timer = 1000; # XX/1000 seconds

# Default values for ye ole cmd-line args.
my $quiet = "no";
my $init_to_dflts = "yes";

my $latency = 35; # miliseconds
my $jitter = 10;
my $reorder = 0;
my $smoothing_buffer = 20000; # XXk smoothing buffer
my $drop_freq = 0;
my $dup_freq = 0;
my $max_wlrate = 1000000000;
my $wl_kmode = 1; # Set to 0 for user-space mode, 1 for kernel mode

# WanPath related settings.
my $max_wp_rate = 10000000;
my $wp_ip_base = "172.2.2";
my $wp_ip_lcb  = 2;
my $wp_ip_mask = "255.255.255.255";
my $wp_lat = 10;
my $wp_jitter = 10;
my $wp_extra_buf = 512;
my $wp_reord = 0;
my $wp_dup = 0;
my $wp_drop = 0;


# Dest matches all
my $wp_dst      = "0.0.0.0";
my $wp_dst_mask = "0.0.0.0";

my $wp_count = 128;

my $fail_msg = "";
my $manual_check = 0;

#my $cmd_log_name = "lf_ice.txt";
#open(CMD_LOG, ">$cmd_log_name") or die("Can't open $cmd_log_name for writing...\n");
#print "History of all commands can be found in $cmd_log_name\n";

########################################################################
# Nothing to configure below here, most likely.
########################################################################

my $usage = "$0  [--quiet {yes | no}]
                 [--init_to_dflts {yes | no}]

Example:
 $0 --init_to_dflts yes\n";


GetOptions (
   'mgr|m=s'      => \$lfmgr_host,
   'port|p=i'     => \$lfmgr_port,
   'quiet|q=s'    => \$quiet,
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
if ($quiet eq "yes") {
  $utils->cli_rcv_silent(1);  # Repress output from CLI ??
}
else {
  $utils->cli_rcv_silent(0);  # Repress output from CLI ??
}


my $dt = "";

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
my $cmd = "";


my $ep1 = "wan1-A";
my $ep2 = "wan1-B";

@endpoint_names = (@endpoint_names, $ep1, $ep2);

# Create the two LANforge-ICE endpoints.
$cmd = "add_wl_endp $ep1 $shelf_num $ice_card $ice1 $latency $max_wlrate";
$utils->doCmd($cmd);
$cmd = "set_wanlink_info $ep1 $max_wlrate $latency $jitter $reorder $smoothing_buffer $drop_freq $dup_freq";
$utils->doCmd($cmd);

# Create the two LANforge-ICE endpoints.
$cmd = "add_wl_endp $ep2 $shelf_num $ice_card $ice2 $latency $max_wlrate";
$utils->doCmd($cmd);
$cmd = "set_wanlink_info $ep2 $max_wlrate $latency $jitter $reorder $smoothing_buffer $drop_freq $dup_freq";
$utils->doCmd($cmd);

$utils->doCmd("set_endp_flag $ep1 KernelMode $wl_kmode");
$utils->doCmd("set_endp_flag $ep2 KernelMode $wl_kmode");



# Add the ICE cross connect.
my $cx_name = "wanlink1";
$cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
$utils->doCmd($cmd);
$utils->doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");

@cx_names = (@cx_names, $cx_name);

# Add the wanpaths
for ($i = 0; $i<$wp_count; $i++) {
  # Add wanpath with specified source and ANY dest.
  $cmd = "add_wanpath $ep1 wp$wp_ip_lcb $max_wp_rate $wp_lat $wp_jitter $wp_extra_buf $wp_reord $wp_drop $wp_dup ${wp_ip_base}.$wp_ip_lcb $wp_ip_mask $wp_dst $wp_dst_mask OFF 'NA'  YES  NO  NO  NO";
  $utils->doCmd($cmd);
  # Add wanpath with specified dest and ANY source.
  $cmd = "add_wanpath $ep2 wp$wp_ip_lcb $max_wp_rate $wp_lat $wp_jitter $wp_extra_buf $wp_reord $wp_drop $wp_dup 0.0.0.0 0.0.0.0 ${wp_ip_base}.$wp_ip_lcb $wp_ip_mask OFF 'NA'  YES  NO  NO  NO";
  $utils->doCmd($cmd);

  $wp_ip_lcb++;
}



for ($i = 0; $i<@cx_names; $i++) {
  my $nm = $cx_names[$i];
  $cmd = "set_cx_state $test_mgr $nm RUNNING";
  $utils->doCmd($cmd);
}

sleep(24 * 60 * 60); # Run for one day

# Stop cxs.
for ($i = 0; $i<@cx_names; $i++) {
  my $nm = $cx_names[$i];
  $cmd = "set_cx_state $test_mgr $nm STOPPED";
  $utils->doCmd($cmd);
}

exit(0);


sub initToDefaults {
  # Clean up database if stuff exists

  $utils->doCmd("rm_cx $test_mgr all");
  $utils->doCmd("rm_endp YES_ALL");
  $utils->doCmd("rm_test_mgr $test_mgr");

}#initToDefaults


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

  # Nothing to do at this point.

}#setUpPorts


sub setUpPort {
  my $sn = shift;
  my $cn = shift;
  my $pn = shift;
  my $ip = shift;
  my $msk = shift;
  my $gw = shift;

  my $cmd = "set_port $sn $cn $pn $ip $msk $gw NA NA NA";
  $utils->doCmd($cmd);
  my $p1 = new LANforge::Port();
  # Tell the port what it is so it decodes the right one..
  $utils->updatePort($p1, $sn, $cn, $pn);
  # Make sure the values we attempted to set actually worked.
  verifyPortAttributes($p1, $sn, $cn, $pn, $ip, $msk, $gw);
}#setUpPort


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
