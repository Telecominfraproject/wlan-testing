#!/usr/bin/perl

# This program is used to stress test the LANforge system, and may be used as
# an example for others who wish to automate LANforge tests.

# This script sets up connections of types:
#   lf, lf_udp, lf_tcp, custom_ether, custom_udp, and custom_tcp
# across 1 real port and manny macvlan ports on 2 machines.
# It then continously starts and stops the connections.

# Un-buffer output
$| = 1;

use strict;

use Net::Telnet ();
use LANforge::Port;
use LANforge::Utils;
use LANforge::Endpoint;

my $lfmgr_host = "localhost";
my $lfmgr_port = 4001;

my $shelf = 1;

# This sets up connections between 2 LANforge machines
my $lf1 = 1;

my $lf2 = 2;  # We also have a second machine to create mac-vlans on.
#my $lf2 = ""; # Set to "" if we have no second machine, can only do l4
#              # endpoints in this case.

# Port pairs.  These are the ports that should be talking to each other.
# Ie, the third column in lf1_ports talks to the third column in lf2_ports.
my @lf1_ports = (5); #, 2, 3);
my @lf2_ports = (5); #, 2, 3);

#  These are for the IP port, the initial value....
my $port_nums = 5000;

my $ip_base = "172.1";
my $ip_lsb = 2;
my $ip_c = 2;
my $msk = "255.255.0.0";

my $num_macvlans = 50;

# If zero, will have one of EACH of the cx types on each port.
#my $one_cx_per_port = 1;
my $one_cx_per_port = 0;

my $mn_sz = 1000;
my $mx_sz = 1000;

# 10 of each, on each port/macvlan   With 100 mac-vlans, yields 1000 sessions.
my @cx_types =     ("lf_udp", "lf_tcp", "lf_udp", "lf_tcp", "lf_udp",
		    "lf_tcp", "lf_udp", "lf_tcp", "lf_udp", "lf_tcp" );
my @min_pkt_szs =  ($mn_sz,    $mn_sz,    $mn_sz,   $mn_sz,   $mn_sz,
		    $mn_sz,   $mn_sz,    $mn_sz,   $mn_sz,   $mn_sz);
my @max_pkt_szs =  ($mx_sz,    $mx_sz,    $mx_sz,   $mx_sz,   $mx_sz,
		    $mx_sz,   $mx_sz,    $mx_sz,   $mx_sz,   $mx_sz);

# Layer-4 only
#my @cx_types =     ("l4", "l4");
#my @min_pkt_szs =  (0, 0);
#my @max_pkt_szs =  (0, 0);

# URL will be acted on from machine $lf1
#my $l4_url = "http://172.1.5.75";
my $l4_url = "http://172.1.2.3";

my $min_rate = 24000;
my $max_rate = 24000;

my $test_mgr = "ben_tm";

my $loop_max = 100;
my $start_stop_iterations = 10000;
my $run_for_time = 0;  # Run for XX seconds..then will be stopped again
my $stop_for_time = 1;  # Run for XX seconds..then will be stopped again
my $report_timer = 5000; # 5 seconds
my $stop_at_connections = 100000;


########################################################################
# Nothing to configure below here, most likely.
########################################################################

my @endpoint_names = (); #will be added to as they are created
my @cx_names = ();

my $tot_cx_started = 0;


# Open connection to the LANforge server.

my $t = new Net::Telnet(Prompt => '/default\@btbits\>\>/');


$t->open(Host    => $lfmgr_host,
	 Port    => $lfmgr_port,
	 Timeout => 45);

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

  initToDefaults();
  #exit(0);

  # Now, add back the test manager we will be using
  doCmd("add_tm $test_mgr");
  doCmd("tm_register $test_mgr default");  #Add default user
  doCmd("tm_register $test_mgr default_gui");  #Add default GUI user

  addMacVlans();

  # Add some IP addresses to the ports
  initIpAddresses();

  # Add our endpoints
  addCrossConnects();

  my $begin_time = time();

  my $was_rcv_silent = $utils->cli_rcv_silent();
  my $was_send_silent = $utils->cli_send_silent();

  $utils->cli_rcv_silent(1);

  my $rl = 0;
  for ($rl = 0; $rl<$start_stop_iterations; $rl++) {

    my $stime = time();
    my $slp = 0;

    $utils->cli_send_silent($was_send_silent);
    doCmd("set_cx_state $test_mgr all RUNNING", 0, 1);
    $utils->cli_send_silent(1);

    #sleep(1); # Give the servers a chance to get started...

    if ($run_for_time == 0) {
      # Stop test as soon as all have received a packet.
      my $i;
      my $endp1 = new LANforge::Endpoint();
      for ($i = 0; $i<@endpoint_names; $i++) {
	my $en = $endpoint_names[$i];
	$utils->updateEndpoint($endp1, $en, 1);
	while ($endp1->rx_pkts() <= 0) {
	  if (time() > $stime + 15) {
	    # Things are not working right, it should never take this long
	    print "WARNING:  Endpoint $en is not receiving packets after $slp seconds.\n";
	    exit 0;
	  }
	  $utils->updateEndpoint($endp1, $en, 1);
	}
      }

      # Stop cxs.
      $utils->cli_send_silent($was_send_silent);
      doCmd("set_cx_state $test_mgr all STOPPED", 0, 1);
      $utils->cli_send_silent(1);

      my $elapsed = time() - $stime;
      my $tot_elapsed = time() - $begin_time;

      $i = @cx_names;
      $tot_cx_started += $i;
      print "\nStarted and stopped $i connections this round in $elapsed seconds.\n";
      print "Started and stopped a total of $tot_cx_started in $tot_elapsed seconds.\n ";
      print $tot_cx_started / $tot_elapsed . " connections per second...\n\n";

      if ($tot_cx_started >= $stop_at_connections) {
	exit 0;
      }

      # Now, lets change the port numbers around.
      for ($i = 0; $i<@endpoint_names; $i++) {
	my $en = $endpoint_names[$i];

	my $cmd = "add_endp $en NA NA NA NA $port_nums NA NA NA NA NA NA NA NA";
	$port_nums = nextPortNum($port_nums);
	doCmd($cmd, 1, 1);
      }#for

    }
    else {

      print "Done starting endpoints...sleeping $run_for_time seconds.\n";
      sleep($run_for_time);

      # Now, stop them...
      if (($rl % 2) == 0) {
	doCmd("set_cx_state $test_mgr all STOPPED");
      }
      else {
	# Do one at a time
	my $q = 0;
	for ($q = 0; $q<@cx_names; $q++) {
	  my $cmd = "set_cx_state $test_mgr " . $cx_names[$q] . " STOPPED";
	  doCmd($cmd);
	}
      }

      sleep($stop_for_time);
    }

  }# For some amount of start_stop iterations...
}# for some amount of loop iterations

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


sub addMacVlans {
  my $i;
  my $q;

  my $v;
  my $lsb = 10;
  my $lsb2 = 10;

  my $throttle = 25;
  my $since_throttle = 0;
  for ($q = 0; $q<@lf1_ports; $q++) {
    my $pnum1 = $lf1_ports[$q];
    my $pnum2 = $lf2_ports[$q];
    for ($i = 0; $i<$num_macvlans; $i++) {

      $lsb++;
      if ($lsb > 99) {
	$lsb2++;
	$lsb = 2;
      }

      my $s2 = $shelf+10;
      my $c2 = $lf1+10;
      my $p2 = $pnum1+10;
      my $mc = "00:$s2:$c2:$p2:$lsb2:$lsb";
      doCmd("add_mvlan $shelf $lf1 $pnum1 $mc");

      if ($lf2 ne "") {
	$c2 = $lf2+10;
	$p2 = $pnum2+10;
	$mc = "00:$s2:$c2:$p2:$lsb2:$lsb";
	doCmd("add_mvlan $shelf $lf2 $pnum2 $mc");

	# Throttle ourself so we don't over-run the poor LANforge system.
	
	if ($since_throttle++ > $throttle) {
	  my $p1 = new LANforge::Port();
	  $utils->updatePort($p1, $shelf, $lf1, $pnum1);

	  my $p1 = new LANforge::Port();
	  $utils->updatePort($p1, $shelf, $lf2, $pnum2);
	  $since_throttle = 0;
	}
      }
    }
  }

  doCmd("probe_ports");

  # Wait untill we discover all the ports...

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

    for ($i = 0; $i<$num_macvlans; $i++) {
      while (1) {
	$utils->updatePort($p1, $shelf, $lf1, "$pname\#$i");
	if ($lf2 ne "") {
	  $utils->updatePort($p2, $shelf, $lf2, "$pname2\#$i");
	}
	if ($p1->isPhantom() || (($lf2 ne "") && $p2->isPhantom())) {
	  sleep(1);
	}
	else {
	  last;
	}
      }
    }
  }


}#addMacVlans


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

    if ($ip_lsb > 250) {
      $ip_c++;
      $ip_lsb = 2;
    }

    my $tmp = $lf1_ports[$i];
    my $tmp2 = $lf2_ports[$i];
    my $cmd = "set_port $shelf $lf1 $tmp $ip_base.$ip_c.$ip_lsb $msk " .
              "$ip_base.1.1 NA NA NA";
    doCmd($cmd);
    $ip_lsb++;

    if ($lf2 ne "") {
      $cmd = "set_port $shelf $lf2 $tmp2 $ip_base.$ip_c.$ip_lsb $msk " .
	"$ip_base.1.1 NA NA NA";
      doCmd($cmd);
      $ip_lsb++;
    }

    my $p1 = new LANforge::Port();
    $utils->updatePort($p1, $shelf, $lf1, $tmp);
    my $pname = $p1->{dev};

    my $q;
    my $throttle = 25;
    my $since_throttle = 0;
    for ($q = 0; $q<$num_macvlans; $q++) {
      $cmd = "set_port $shelf $lf1 $pname\#$q $ip_base.$ip_c.$ip_lsb $msk " .
	     "$ip_base.1.1 NA NA NA";
      doCmd($cmd);
      $ip_lsb++;

      if ($ip_lsb > 250) {
	$ip_c++;
	$ip_lsb = 2;
      }

      if ($since_throttle++ > $throttle) {
	my $p1 = new LANforge::Port();
	$utils->updatePort($p1, $shelf, $lf1, "$pname\#$q");	
	$since_throttle = 0;
      }

    }

    $ip_lsb++;

    if ($lf2 ne "") {
      $p1 = new LANforge::Port();
      $utils->updatePort($p1, $shelf, $lf2, $tmp2);
      $pname = $p1->{dev};

      for ($q = 0; $q<$num_macvlans; $q++) {
	$cmd = "set_port $shelf $lf2 $pname\#$q $ip_base.$ip_c.$ip_lsb $msk " .
	  "$ip_base.1.1 NA NA NA";
	doCmd($cmd);
	$ip_lsb++;
	
	if ($ip_lsb > 250) {
	  $ip_c++;
	  $ip_lsb = 2;
	}
	
	if ($since_throttle++ > $throttle) {
	  my $p1 = new LANforge::Port();
	  $utils->updatePort($p1, $shelf, $lf2, "$pname\#$q");	
	  $since_throttle = 0;
	}
      }
    }# If we have an LF-2 defined.
  }
}

sub addCrossConnects {
  my $ep = 0;
  my $cx = 0;
  my $i = 0;


  my @all_ports1 = @lf1_ports;
  my $j;
  my $pname;
  for ($j = 0; $j<@lf1_ports; $j++) {
    my $p1 = new LANforge::Port();
    $utils->updatePort($p1, $shelf, $lf1, $lf1_ports[$j]);
    $pname = $p1->{dev};

    my $q;
    for ($q = 0; $q<$num_macvlans; $q++) {
      @all_ports1 = (@all_ports1, "$pname\#$q");
    }
  }

  my @all_ports2 = @lf2_ports;
  if ($lf2 ne "") {
    for ($j = 0; $j<@lf2_ports; $j++) {
      my $p1 = new LANforge::Port();
      $utils->updatePort($p1, $shelf, $lf2, $lf2_ports[$j]);
      $pname = $p1->{dev};

      my $q;
      for ($q = 0; $q<$num_macvlans; $q++) {
	@all_ports2 = (@all_ports2, "$pname\#$q");
      }
    }
  }

  print "About to start endpoints, all_ports1:\n" . join(" ", @all_ports1) .
        "\nall_ports2: " . join(" ", @all_ports2) . "\n\n";

  if ($one_cx_per_port) {
    my $j = 0;
    my $cxcnt = 0;
    for ($j ; $j<@all_ports1; $j++) {
      my $i = $cxcnt % @cx_types;
      $cxcnt++;

      my $cxt = $cx_types[$i];
      if ($cxt eq "l4") {
	# Create layer-4 endpoint
	
	my $ep1 = "endp-${ep}-TX";
	$ep++;
	my $ep2 = "D_endp-${ep}-TX";
	$ep++;
	
	@endpoint_names = (@endpoint_names, $ep1, $ep2);

	# Add the dummy endpoint
	my $cmd = "add_l4_endp $ep2 $shelf $lf1 " . $all_ports1[$j] . " l4_generic  0 0 0 ' ' ' '";
	doCmd($cmd);
	$cmd = "set_endp_flag $ep2 unmanaged 1";
	doCmd($cmd);

	$cmd = "add_l4_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " l4_generic 0 10000 100 '" .
	  "dl $l4_url /tmp/$ep1' ' '";
	doCmd($cmd);

	# Now, add the cross-connects
	my $cx_name = "cx-${cx}";
	$cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
	doCmd($cmd);
	doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");
	
	$cx++;
	
	@cx_names = (@cx_names, $cx_name);
      }
      else {
	my $burst = "NO";
	if ($min_rate != $max_rate) {
	  $burst = "YES";
	}
	my $szrnd = "NO";
	if ($min_pkt_szs[$i] != $max_pkt_szs[$i]) {
	  $szrnd = "YES";
	}
	
	my $pattern = "increasing";
	if ($cx_types[$i] =~ /custom/) {
	  $pattern = "custom";
	}
	
	my $ep1 = "endp-${ep}-TX";
	$ep++;
	my $ep2 = "endp-${ep}-RX";
	$ep++;
	
	@endpoint_names = (@endpoint_names, $ep1, $ep2);
	
	my $cmd = "add_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " " . @cx_types[$i] .
	    " $port_nums $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " . $max_pkt_szs[$i] .
	    " $pattern NO";
	$port_nums = nextPortNum($port_nums);
	doCmd($cmd);


	if ($lf2 == "") {
	  die("Must have lf2 defined if using non-l4 endpoints.");
	}
	
	$cmd =    "add_endp $ep2 $shelf $lf2 " . $all_ports2[$j] . " " . @cx_types[$i] .
	    " $port_nums $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " .
	    $max_pkt_szs[$i] . " $pattern NO";
	$port_nums = nextPortNum($port_nums);
	doCmd($cmd);
	
	# Now, add the cross-connects
	my $cx_name = "cx-${cx}";
	$cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
	doCmd($cmd);
	doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");
	
	$cx++;

	@cx_names = (@cx_names, $cx_name);
      }
    }#for all ports
  }#one_cx_per_port
  else {
    my $j = 0;
    for ($j ; $j<@all_ports1; $j++) {
      for ($i = 0; $i<@cx_types; $i++) {
	my $cxt = $cx_types[$i];

	if ($cxt eq "l4") {
	  # Create layer-4 endpoint
	
	  my $ep1 = "endp-${ep}-TX";
	  $ep++;
	  my $ep2 = "D_endp-${ep}-TX";
	  $ep++;
	
	  @endpoint_names = (@endpoint_names, $ep1, $ep2);
	
	  # Add the dummy endpoint
	  my $cmd = "add_l4_endp $ep2 $shelf $lf1 " . $all_ports1[$j] . " l4_generic  0 0 0 ' ' ' '";
	  doCmd($cmd);
	  $cmd = "set_endp_flag $ep2 unmanaged 1";
	  doCmd($cmd);
	
	  $cmd = "add_l4_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " l4_generic 0 10000 100 '" .
	       "dl $l4_url /tmp/$ep1' ' '";
	  doCmd($cmd);

	  # Now, add the cross-connects
	  my $cx_name = "cx-${cx}";
	  $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
	  doCmd($cmd);
	  doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");
	
	  $cx++;
	
	  @cx_names = (@cx_names, $cx_name);
	}
	else {
	  my $burst = "NO";
	  if ($min_rate != $max_rate) {
	    $burst = "YES";
	  }
	  my $szrnd = "NO";
	  if ($min_pkt_szs[$i] != $max_pkt_szs[$i]) {
	    $szrnd = "YES";
	  }
	
	  my $pattern = "increasing";
	  if ($cx_types[$i] =~ /custom/) {
	    $pattern = "custom";
	  }
	
	  my $ep1 = "endp-${ep}-TX";
	  $ep++;
	  my $ep2 = "endp-${ep}-RX";
	  $ep++;
	
	  @endpoint_names = (@endpoint_names, $ep1, $ep2);
	
	  my $cmd = "add_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " " . @cx_types[$i] .
	    " $port_nums $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " . $max_pkt_szs[$i] .
	      " $pattern NO";
	  $port_nums = nextPortNum($port_nums);
	  doCmd($cmd);

	  if ($lf2 == "") {
	    die("Must lave lf2 defined if using non-l4 endpoints.");
	  }
	
	  $cmd =    "add_endp $ep2 $shelf $lf2 " . $all_ports2[$j] . " " . @cx_types[$i] .
	    " $port_nums $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " .
	      $max_pkt_szs[$i] . " $pattern NO";
	  $port_nums = nextPortNum($port_nums);
	  doCmd($cmd);
	
	  # Now, add the cross-connects
	  my $cx_name = "cx-${cx}";
	  $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
	  doCmd($cmd);
	  doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");
	
	  $cx++;
	
	  @cx_names = (@cx_names, $cx_name);
	}
      }#for cx types
    }#for each port
  }# each cx per port

}#addCrossConnects


sub nextPortNum {
  my $cur = shift;
  if ($cur > 65033) {
    return int(rand(1000) + 5000);
  }
  $cur++;
  return $cur;
}

sub doCmd {
  my $cmd = shift;
  my $send_silent = shift;
  my $rcv_silent = shift;

  if (! $send_silent) {
    print ">>> $cmd\n";
  }

  $t->print($cmd);
  my @rslt = $t->waitfor('/ \>\>RSLT:(.*)/');
  if (! $rcv_silent) {
    print "**************\n @rslt ................\n\n";
  }
  #sleep(1);
}
