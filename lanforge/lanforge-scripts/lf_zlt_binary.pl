#!/usr/bin/perl

# IMIX Zero Loss Throughput Test
# Uses a binary search algorithm to determine the throughput at which
# zero packet loss occurs for a given theoretical throughput rate
# and max allowable latency.
#
# USAGE: 
# perl lf_zlt_binary.pl lf_host theoretical_rate max_latency
# binary_search_attempts endpoint_duration test_loops
#
# Example: perl lf_zlt_binary.pl 192.168.100.192 10000000 200 9 10 1


# Un-buffer output
$| = 1;

use strict;

use Net::Telnet ();
use LANforge::Port;
use LANforge::Utils;
use LANforge::Endpoint;

my $lfmgr_host = "$ARGV[0]"; #localhost or IP
my $lfmgr_port = 4001;

my $shelf = 1;

# The LANforge resources
my $lf1 = 1;
my $lf2 = 1;

# Port pairs.  These are the ports that should be talking to each other.
# Ie, lf1_ports talks to lf2_ports.
my @lf1_ports = (6);
my @lf2_ports = (7);

my @lf1_port_ips = ("172.1.1.6");
my @lf2_port_ips = ("172.1.1.7");

my @lf1_port_gws = ("172.1.1.1");
my @lf2_port_gws = ("172.1.1.1");

# IMIX Type Definition for UDP
# Packet sizes are in bytes of UDP payload
my @cx_types = ("lf_udp", "lf_udp", "lf_udp", "lf_udp", "lf_udp", "lf_udp", "lf_udp", "lf_udp");
my @min_pkt_szs =  (22, 86, 214, 470, 982, 1238, 1458, 1472);
my @max_pkt_szs =  (22, 86, 214, 470, 982, 1238, 1458, 1472);

# Network Under Test Maximum Theoretical Throughput
my $min_rate = $ARGV[1]; # a rate such as 1544000
my $max_rate = $ARGV[1];

# Maximum Latency in miliseconds, allowed before adjusting rate down 
my $max_latency = $ARGV[2]; # in milliseconds

my $test_mgr = "zlt_tm";

my $binary_search_attempts = $ARGV[3]; # number of attempts to find zlt for a given pkt size
my $pause_sec = 10; # seconds for endpoints to update
my $endp_duration = $ARGV[4]; # seconds endpoints are allowed to run, can affect results
my $loop_max = $ARGV[5]; # number of times the entire test will be run
my $report_timer = 1000; 
my @endp_drops = ();

if (@ARGV != 6) {
  print("USAGE: perl lf_zlt_binary.pl lf_host theoretical_rate max_latency ");
  print("binary_search_attempts endpoint_duration test_loops\n");
  print("Example: perl lf_zlt_binary.pl 192.168.100.192 10000000 200 ");
  print("9 10 1\n");
  exit 1;
}

########################################################################
# Nothing to configure below here, most likely.
########################################################################

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
  print "Pause $pause_sec seconds for ports to update.\n";
  sleep($pause_sec);

  # Start Cross-Connects
  for (my $q=0; $q<@cx_names; $q++) {
    my $cmd = "set_cx_state $test_mgr " . $cx_names[$q] . " RUNNING";
    doCmd($cmd);

    my @next_adj = (int($max_rate / 2), int($max_rate / 2));
    my @current_rate = ($max_rate, $max_rate);
    my $last_current_rate = 0;
    my @new_rate = (0,0);
    my $adj_count = 0;
    my $p1 = $q+$q;
    my $p2 = $p1+1;


    for ($adj_count=0; $adj_count < $binary_search_attempts; $adj_count++) {

      doCmd("clear_endp_counters");
      print "sleep $endp_duration seconds\n";
      sleep($endp_duration);

      for (my $p=$p1; $p<=$p2; $p++) {
         my $endp1 = new LANforge::Endpoint();
         $utils->updateEndpoint($endp1, $endpoint_names[$p]);
         my $en1 = $endp1->rx_dropped_pkts();
         my $en2 = $endp1->port_id();
         my $en3 = $endp1->real_rx_rate();
         my $lat = $endp1->avg_latency();

         my $i = $p-$p1;
	 if ( $en1 != 0 || $lat > $max_latency ) {
           print "Drops! en1 is $en1 : en2 is $en2 : Real RX Rate is: $en3 : Latency: $lat\n";
           $new_rate[$i] = $current_rate[$i] - $next_adj[$i];
         }
         elsif ( $current_rate[$i] < $max_rate ) {
           print "No Drops! en1 is $en1 : en2 is $en2 : Real RX Rate is: $en3 : Latency: $lat\n";
           $last_current_rate = $current_rate[$i];
           $new_rate[$i] = $current_rate[$i] + $next_adj[$i];
	 }
         else {
           print "Max Rate of $max_rate bps is too high for $min_pkt_szs[$q] byte packet size.\n";
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
       sleep(3);

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
    print "\n\n*********************************************************\n";
    print "Theoretical Throughput: $min_rate bps.\n";
    print "Zero-Loss Throughput: $last_current_rate bps for $min_pkt_szs[$q] byte packets.\n\n";
    sleep(10);

  } #for cross-connects  
} #for $loop_max

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



  doCmd("probe_ports");

  # Wait untill we discover all the ports...

  my $q=0;
  for ($q = 0; $q<@lf1_ports; $q++) {
    my $p1 = new LANforge::Port();
    $utils->updatePort($p1, $shelf, $lf1, $lf1_ports[$q]);
    my $pname = $p1->{dev};

    my $p2 = new LANforge::Port();
    my $pname2;
    if ($lf2 ne "") {
      $utils->updatePort($p2, $shelf, $lf2, $lf2_ports[$q]);
      $pname2 = $p2->{dev};
    }
  }



# Wait untill the system can update a port..
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
    print "Found $mx ports for resource: $shelf.$lf1\n";

    if (($mx == 0) || ($utils->error() =~ /Timed out/g)) {
      # System is too backlogged to answer, wait a bit
      print " Will try listing ports again in a few seconds...system is backlogged now!\n";
      sleep(5);
      $found_one = 1;
      next;
    }

    my $throttle = 0;
    my $wait_for_phantom = 0;
    for ($i = 0; $i<$mx; $i++) {
      if ($ports[$i]->isMacVlan()) {
	if ($ports[$i]->isPhantom()) {
	  # Wait a bit..hopefully it will go away.
	  if ($wait_for_phantom++ < 20) {
	    print "Sleeping a bit, found a phantom port.";
	    sleep(5);
	    doCmd("probe_ports");
	    $found_one = 1;
	  }
	}
	else {
	  doCmd($ports[$i]->getDeleteCmd());
	  $found_one = 1;
	}
      }
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
    $cmd = "set_port $shelf $lf2 $tmp2 " . $lf2_port_ips[$i] . " 255.255.255.0 " .              $lf2_port_gws[$i] . " NA NA NA";
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
                " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i]
                . " " . $max_pkt_szs[$i] . " $pattern ";
      doCmd($cmd);

      $cmd =    "add_endp $ep2 $shelf $lf2 " . $lf2_ports[$j] . " " . @cx_types[$i] .
                " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i]
                . " " . $max_pkt_szs[$i] . " $pattern ";
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
