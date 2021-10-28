#!/usr/bin/perl

# IMIX Throughput Test
#
# Uses a binary search algorithm to determine the maximum throughput at which
# a specified percent packet loss occurs and a maximum latency is allowed
# for a given theoretical throughput rate at different packet sizes suggested
# by IMIX literature.
#
# USAGE: perl imix.pl lf_host port-1 port-2 theoretical_rate max_latency
# max_drop_percentage binary_search_attempts endpoint_duration test_loops
#
# Example: perl imix.pl 192.168.100.192 1 2 10000000 200 10 9 10 1

# Un-buffer output
$| = 1;

use strict;

use Net::Telnet ();
use LANforge::Port;
use LANforge::Utils;
use LANforge::Endpoint;

my $script_name = "imix.pl";

my $lfmgr_host = undef;
my $lfmgr_port = 4001;

my $test_mgr = "imix_tm";

my $shelf = 1;

# This sets up connections between 2 LANforge machines
my $lf1 = 1; # Minor Resource EID.
my $lf2 = 1; # Set to "" or same as $lf1 if we have no second machine.  For second machine set
             # to second Resource minor EID to create mac-vlans on it.

# Port pairs.  These are the ports that should be talking to each other.
# i.e. the third column in lf1_ports talks to the third column in lf2_ports.
# EIDs or aliases can be used.
# Port pairs must match on each shelf - will enhance to allow any pair on each shelf.
#my @lf1_ports = (1); #, 2, 3);
#my @lf2_ports = (2); #, 2, 3);
my @lf1_ports = ("eth2"); #, "eth0");
my @lf2_ports = ("eth3"); #, "eth1");

my @lf1_port_ips = ("172.1.1.100");
my @lf2_port_ips = ("172.1.1.101");

my @lf1_port_gws = ("172.1.1.1");
my @lf2_port_gws = ("172.1.1.1");

# IMIX Type Definition for UDP
# Packet sizes are in bytes of UDP payload
my @cx_types =    ("lf_udp", "lf_udp", "lf_udp", "lf_udp", "lf_udp", "lf_udp", "lf_udp", "lf_udp");
my @min_pkt_szs = (      22,       86,      214,      470,      982,     1238,     1458,     1472);
my @max_pkt_szs = (      22,       86,      214,      470,      982,     1238,     1458,     1472);
my @tput_rates  = ( 1000000,  4000000, 12000000, 45000000,155000000,155000000,155000000,155000000);

my $tput = 1544000; # Network/Device Under Test Maximum Theoretical Throughput in bps.

my $max_latency = 1;       # Maximum Latency in miliseconds, allowed before adjusting rate down.
my $drop_percent = 0.0001; # Maximum Drop-Percentage allowed before adjusting rate down.

my $binary_search_attempts = 9; # Number of attempts to find throughput for a given pkt size and $drop_percent.
my $endp_wait_for_update = 10;             # Seconds allowed for endpoints to update.
my $endp_duration = 30;         # Seconds endpoints are allowed to run which can affect results.
my $loop_max = 1;               # Number of times the entire test will be run


my @endp_drops = ();
########################################################################
# Nothing to configure below here, most likely.
########################################################################
# Parse cmd-line args
my $i;
for ($i = 0; $i<@ARGV; $i++) {
  my $var = $ARGV[$i];
  if ($var =~ m/(\S+)=(.*)/) {
    my $arg = $1;
    my $val = $2;
    handleCmdLineArg($arg, $val);
  }
  else {
    handleCmdLineArg($var);
  }
}

if ($lfmgr_host == undef) {
  print "\nYou must define a LANforge Manager!!!\n\n"
      . "For example:\n"
      . "./$script_name mgr=locahost\n"
      . "OR\n"
      . "./$script_name mgr=192.168.1.101\n\n";
  printHelp();
  exit (1);
}


my $min_rate = $tput;
my $max_rate = $min_rate;

my $report_timer = 1000; # Report timer for endpoints.

my @endpoint_names = (); #will be added to as they are created
my @cx_names = ();

# Open connection to the LANforge server.

my $t = new Net::Telnet(Prompt => '/default\@btbits\>\>/');

my $timeout = 60;

$t->open(Host    => $lfmgr_host,
         Port    => $lfmgr_port,
         Timeout => $timeout);

$t->waitfor("/btbits\>\>/");

# Configure our utils.
my $utils = new LANforge::Utils();
$utils->telnet($t);         # Set our telnet object.
$utils->cli_send_silent(0); # Do show input to CLI
$utils->cli_rcv_silent(0);  # Repress output from CLI ??


my $dt = "";

my $loop = 0;
for ($loop = 0; $loop<$loop_max; $loop++) {
  $dt = `date`;
  chomp($dt);
  print "\n\n*****  Starting loop: $loop at: $dt  *****\n\n";

  @endpoint_names = ();
  @cx_names = ();

  initToDefaults();

  # Now, add back the test manager we will be using
  doCmd("add_tm $test_mgr");
  doCmd("tm_register $test_mgr default");  #Add default user
  doCmd("tm_register $test_mgr default_gui");  #Add default GUI user


  # Add some IP addresses to the ports
  initIpAddresses();

  # Add our endpoints
  addCrossConnects();

  print "Loop $loop: Done adding CXs.\n";
  print "Pause $endp_wait_for_update seconds for endpoints to update.\n";
  sleep($endp_wait_for_update);

  # Start Cross-Connects
  for (my $q=0; $q<@cx_names; $q++) {
    my $cmd = "set_cx_state $test_mgr " . $cx_names[$q] . " RUNNING";
    doCmd($cmd);

    my @next_adj = (int($max_rate / 2), int($max_rate / 2));
    my @current_rate = ($max_rate, $max_rate);
    my @last_current_rate = (0,0);
    my @new_rate = (0,0);
    my $flag = 0;
    my $best_rate = 0;
    my $adj_count = 0;
    my $p1 = $q+$q;
    my $p2 = $p1+1;


    for ($adj_count=0; $adj_count < $binary_search_attempts; $adj_count++) {

      doCmd("clear_endp_counters");
      doCmd("clear_cx_counters");
      print "Adjustment Period: $adj_count\n";
      print "sleep $endp_duration seconds\n";
      sleep($endp_duration);

      for (my $p=$p1; $p<=$p2; $p++) {
         my $endp1 = new LANforge::Endpoint();
         $utils->updateEndpoint($endp1, $endpoint_names[$p]);
         my $en1 = $endp1->rx_drop_seq();
         my $en2 = $endp1->port_id();
         my $en3 = $endp1->real_rx_rate();
         my $lat = $endp1->avg_latency();

         my $i = $p-$p1;
	 if ( $en1 > $drop_percent || $lat > $max_latency ) {
           print "RATE DOWN: Percent Dropped is $en1 : Port is $en2 : Real RX Rate is: $en3 : Latency: $lat\n";
           $new_rate[$i] = $current_rate[$i] - $next_adj[$i];
         }
         elsif ( $current_rate[$i] < $max_rate ) {
           print "RATE UP: Percent Dropped is $en1 : Port is $en2 : Real RX Rate is: $en3 : Latency: $lat\n";
           $last_current_rate[$i] = $current_rate[$i];
           $new_rate[$i] = $current_rate[$i] + $next_adj[$i];
	 }
         else {
           # packet size is too small for this LF system to generate at this rate
           # TO DO: make an imix script that uses armageddon instead of user-space UDP
           $best_rate = $en3;
           $flag = 1;
           $adj_count = $binary_search_attempts;
           last;
         }

         $next_adj[$i] = int($next_adj[$i] / 2);
         $current_rate[$i] = $new_rate[$i];

       } #for $endpoint_names

       # set both endpoints to zero rate to quiesce
       my $cmd = "add_endp " . $endpoint_names[$p1] . " $shelf $lf1 " . " NA lf_udp " .
        " -1 NO 0 0 NA NA NA NA ";
       doCmd($cmd);
       $cmd = "add_endp " . $endpoint_names[$p2] . " $shelf $lf1 " . " NA lf_udp " .
        " -1 NO 0 0 NA NA NA NA ";
       doCmd($cmd);
       sleep(5);

       # set both endpoints to new rate
       $cmd = "add_endp " . $endpoint_names[$p1] . " $shelf $lf1 " . " NA lf_udp " .
        " -1 NO " . $new_rate[0] . " " . $new_rate[0] . " NA NA NA NA ";
       doCmd($cmd);
       $cmd = "add_endp " . $endpoint_names[$p2] . " $shelf $lf1 " . " NA lf_udp " .
        " -1 NO " . $new_rate[1] . " " . $new_rate[1] . " NA NA NA NA ";
       doCmd($cmd);
    } #for $adj_count

    doCmd("set_cx_state $test_mgr " . $cx_names[$q] . " STOPPED");
    doCmd("clear_cx_counters");
    doCmd("clear_port_counters");

    if ( $flag != 1 ) {
      print "\n\n*********************************************************\n";
      print "Theoretical Throughput: $max_rate bps.\n";
      print "IMIX Packet Size: $min_pkt_szs[$q] byte payload.\n";
      print "Loss and Latency Allowance: $drop_percent % drops and $max_latency ms latency.\n";
      print "Measured Throughput on Endpoint 1: $last_current_rate[0] bps.\n";
      print "Measured Throughput on Endpoint 2: $last_current_rate[1] bps.\n\n";
      sleep(10);
    }
    else {
      print "\n\nMax Rate of $max_rate bps is too high for $min_pkt_szs[$q] byte packet size.\n";
      print "At $min_pkt_szs[$q] byte packet size, the best user-space rate is: $best_rate bps.\n\n";
    }
  } #for cross-connects
} #for $loop_max

initPortsToDefault();

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

# Wait until the system can update a port..
sub throttleCard {
  my $s = shift;
  my $c = shift;
  my $p1 = new LANforge::Port();
  $utils->updatePort($p1, $s, $c, 1);
}#throttle

sub initPortsToDefault {
  clearMacVlanPorts($shelf, $lf1);
  if ($lf2 ne "") {
    clearMacVlanPorts($shelf, $lf2);
  }

  throttleCard($shelf, $lf1);

  if ($lf2 ne "") {
    throttleCard($shelf, $lf2);
  }

  # Set all ports we are messing with to known state.
  my $i = 0;
  for ($i = 0; $i<@lf1_ports; $i++) {
    my $tmp = $lf1_ports[$i];
    my $tmp2 = $lf2_ports[$i];
    doCmd("set_port $shelf $lf1 $tmp 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
    if ($lf2 ne "") {
      doCmd("set_port $shelf $lf2 $tmp2 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
    }
  }
}

sub clearMacVlanPorts {
  my $s = shift;
  my $c = shift;

  my $i;
  my $found_one = 1;
  my @ports = ();
  while ($found_one) {
    $found_one = 0;
    doCmd("probe_ports");
    # Clear out any existing MAC-VLAN ports.
    $utils->error("");
    @ports = $utils->getPortListing($s, $c);
    my $mx = @ports;
    print "Found $mx ports for card: $shelf.$lf1\n";

    if (($mx == 0) || ($utils->error() =~ /Timed out/g)) {
      # System is too backlogged to answer, wait a bit
      print " Will try listing ports again in a few seconds...system is backlogged now!\n";
      sleep(5);
      $found_one = 1;
      next;
    }

    my $throttle = 0;
    for ($i = 0; $i<$mx; $i++) {
      if ($ports[$i]->isMacVlan()) {
	    doCmd($ports[$i]->getDeleteCmd());
      } #fi isMacVlan
    }
  }
}

sub initIpAddresses {
  # Set all ports we are messing with to known state.
  my $i = 0;
  for ($i = 0; $i<@lf1_ports; $i++) {
    my $tmp = $lf1_ports[$i];
    my $tmp2 = $lf2_ports[$i];
    my $cmd = "set_port $shelf $lf1 $tmp " . $lf1_port_ips[$i] . " 255.255.255.0 " .
               $lf1_port_gws[$i] . " NA NA NA";
    doCmd($cmd);
    $cmd = "set_port $shelf $lf2 $tmp2 " . $lf2_port_ips[$i] . " 255.255.255.0 " .
            $lf2_port_gws[$i] . " NA NA NA";
    doCmd($cmd);
  }
}

sub addCrossConnects {
  my $ep = 0;
  my $cx = 0;
  my $i = 0;
  for ($i = 0; $i<@cx_types; $i++) {
    my $j = 0;
    for ($j = 0; $j<@lf1_ports; $j++) {
      my $burst = "NO";
      my $szrnd = "NO";
      my $pattern = "increasing";

      my $ep1 = "endp-${ep}-TX";
      $ep++;
      my $ep2 = "endp-${ep}-RX";
      $ep++;

      @endpoint_names = (@endpoint_names, $ep1, $ep2);

      my $cmd = "add_endp $ep1 $shelf $lf1 " . $lf1_ports[$j] . " " . @cx_types[$i] .
                " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] .
                " " . $max_pkt_szs[$i] . " $pattern ";
      doCmd($cmd);

      $cmd =    "add_endp $ep2 $shelf $lf2 " . $lf2_ports[$j] . " " . @cx_types[$i] .
                " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] .
                " " . $max_pkt_szs[$i] . " $pattern ";
      doCmd($cmd);

      # Now, add the cross-connects
      my $cx_name = "cx-${cx}";
      $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
      doCmd($cmd);
      doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");

      $cx++;

      @cx_names = (@cx_names, $cx_name);

    }#for all ports
  }#for all endpoint types
}#addCrossConnects


sub doCmd {
  my $cmd = shift;

  print ">>> $cmd\n";

  $t->print($cmd);
  my @rslt = $t->waitfor(Match => '/ \>\>RSLT:(.*)/',
			 Timeout => $timeout);

  print "**************\n @rslt ................\n\n";
  #sleep(1);
}

sub printHelp {
  print "\n"
      . "USAGE:  mgr=[ip-of-mgr] lf1=X lf2=Y\n"
      . "        lf1_ports=[\"1 2 3\"|\"eth2 eth3\"] lf2_ports=[\"4 5 6\"|\"eth4 eth5\"]\n"
      . "        rate=1544000 (bps) max_delay=1 (ms) max_drop=0.0001 (%) search_tries=9\n"
      . "        ep_wait=10 (s) ep_run=30 (s) imix_loops=1\n"
      . "\n";

}

sub handleCmdLineArg {
  my $arg = $_[0];
  my $val = $_[1];

  if ($arg eq "mgr") {
    $lfmgr_host = $val;
  }
  elsif ($arg eq "lf1") {
    $lf1 = $val;
  }
  elsif ($arg eq "lf2") {
    $lf2 = $val;
  }
  elsif ($arg eq "lf1_ports") {
    @lf1_ports = split(/ /, $val);
  }
  elsif ($arg eq "lf2_ports") {
    @lf2_ports = split(/ /, $val);
  }
  elsif ($arg eq "rate") {
    $tput = $val;
  }
  elsif ($arg eq "max_delay") {
    $max_latency = $val;
  }
  elsif ($arg eq "max_drop") {
    $drop_percent = $val;
  }
  elsif ($arg eq "search_tries") {
    $binary_search_attempts = $val;
  }
  elsif ($arg eq "ep_wait") {
    $endp_wait_for_update = $val;
  }
  elsif ($arg eq "ep_run") {
    $endp_duration = $val;
  }
  elsif ($arg eq "imix_loops") {
    $loop_max = $val;
  }
  else {
    printHelp();
    exit(1);
  }
} # handleCmdLineArg
