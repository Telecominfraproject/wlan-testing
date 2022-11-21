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

my $lfmgr_host = "localhost";
my $lfmgr_port = 4001;

my $shelf = 1;

# Set up connections between 2 LANforge machines
# ==============================================
my $INIT = 1; # If true, removes all previous tests!!!

my $lf1 = 1;
#my $lf2 = 4;  # We also have a second machine to create mac-vlans on.
my $lf2 = ""; # Set to "" if we have no second machine, can only do l4
              # endpoints in this case.

# Port pairs.  These are the ports that should be talking to each other.
# Ie, the third column in lf1_ports talks to the third column in lf2_ports.
my @lf1_ports = (0); #, 2, 3);
my @lf2_ports = (0); #, 2, 3);

my $ip_base = "172.29";
my $ip_lsb = 110;
my $ip_c = 3;
my $msk = "255.255.0.0";

my $use_mac_vlans = 1; # set to 1 for MAC-VLANS.  Will use 8021q otherwise.
my $num_vlans = 100;
my $starting_vid = 1000;

# If zero, will have one of EACH of the cx types on each port.
#my $one_cx_per_port = 1;
my $one_cx_per_port = 0;

#my @cx_types =     ("lf", "lf_udp", "lf_tcp", "custom_udp", "custom_tcp", "l4");
#my @min_pkt_szs =  (64,   1,        1,         1,            1,            0);
#my @max_pkt_szs =  (1514, 12000,    13000,     2048,         2048,         0);

#my @cx_types =     ("lf_tcp");
#my @min_pkt_szs =  (1);
#my @max_pkt_szs =  (13000);

# Layer-4 only
#my @cx_types =     ("l4", "l4", "l4"); #, "l4", "l4");
#my @min_pkt_szs =  (0, 0, 0); #, 0, 0);
#my @max_pkt_szs =  (0, 0, 0); #, 0, 0);
my @cx_types =     ("l4"); #, "l4", "l4");
my @min_pkt_szs =  (0); #, 0, 0);
my @max_pkt_szs =  (0); #, 0, 0);

# URL will be acted on from machine $lf1
#my $l4_url = "http://192.168.3.148/index.html";
my $l4_url = "http://www.candelatech.com/oss/pktgen.c";
my $save_to_dev_null = 1; # Set to zero if you want to save http files to /tmp/$ep1

my $min_rate = 64000;
#my $max_rate = 512000;
my $max_rate = 64000;
my $url_per_10m = 600; # 600 is 1 request per second
my $test_mgr = "ben_tm";

my $loop_max = 100000;
my $start_stop_iterations = 1;
my $run_for_time = 2000;  # Run for XX seconds..then will be stopped again
my $stop_for_time = 5;  # Run for XX seconds..then will be stopped again
my $report_timer = 8000; # 8 seconds


########################################################################
# Nothing to configure below here, most likely.
########################################################################
my @num = (); #make sorting by name easier :P
my $total_mvlans = (($num_macvlans+1)*2);
my $num_len = length ($total_mvlans);
use Switch;
my $i = 0;

  switch ($num_len) {
    case 1 {
      for ($i=0;$i<$total_mvlans;$i++) {
	$num[$i] = sprintf("%01d", $i);
      }
    }
    case 2 {
      for ($i=0;$i<$total_mvlans;$i++) {
	$num[$i] = sprintf("%02d", $i);
      }
    }
    case 3 {
      for ($i=0;$i<$total_mvlans;$i++) {
	$num[$i] = sprintf("%03d", $i);
      }
    }
    case 4 {
      for ($i=0;$i<$total_mvlans;$i++) {
	$num[$i] = sprintf("%04d", $i);
      }
    }
    else { print '***** Error Invalid Number of MAC VLANS i.e. >10,000 !!!!'; }
  }
#my $junk=0;
#      for ($junk=0;$junk<$total_mvlans;$junk++) {
#	printf "$num[$junk],";
#      }
#printf "\n";

#exit(0);

my @endpoint_names = (); #will be added to as they are created
my @cx_names = ();

# Open connection to the LANforge server.

my $t = new Net::Telnet(Timeout => 45,
			Prompt => '/default\@btbits\>\>/');


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
  @endpoint_names = ();
  @cx_names = ();

  $dt = `date`;
  chomp($dt);
  print "\n\n*****  Starting loop: $loop at: $dt  *****\n\n";

  if ($INIT) {
  	initToDefaults();
  }
  #exit(0);

  # Now, add back the test manager we will be using
  doCmd("add_tm $test_mgr");
  doCmd("tm_register $test_mgr default");  #Add default user
  doCmd("tm_register $test_mgr default_gui");  #Add default GUI user

  if ($use_mac_vlans) {
    addMacVlans();
  }
  else {
    add8021qVlans();
  }

  # Add some IP addresses to the ports
  initIpAddresses();

  # Add our endpoints
  addCrossConnects();

  my $rl = 0;
  #for ($rl = 0; $rl<$start_stop_iterations; $rl++) {
  for ($rl = 0; $rl<$loop; $rl++) {
    if (($rl % 2) == 0) {
      doCmd("set_cx_state $test_mgr all RUNNING");
    }
    else {
      # Do one at a time
      my $q = 0;
      for ($q = 0; $q<@cx_names; $q++) {
	my $cmd = "set_cx_state $test_mgr " . $cx_names[$q] . " RUNNING";
	doCmd($cmd);
      }
    }

    print "Done starting endpoints...sleeping $run_for_time seconds.\n";
    sleep($run_for_time);

    # Drop the ports.. (Testing kernel bug fix. )
    if ($loop % 2 == 0) {
      clearVlanPorts($shelf, $lf1);
    }

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
    for ($i = 0; $i<$num_vlans; $i++) {

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

    for ($i = 0; $i<$num_vlans; $i++) {
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


sub add8021qVlans {
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
    for ($i = 0; $i<$num_vlans; $i++) {

      $lsb++;
      if ($lsb > 99) {
	$lsb2++;
	$lsb = 2;
      }
      my $vid = $starting_vid + $i;
      doCmd("add_vlan $shelf $lf1 $pnum1 $vid");

      if ($lf2 ne "") {
	$vid = $starting_vid + $num_vlans + $i;
	doCmd("add_vlan $shelf $lf2 $pnum2 $vid");

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

    for ($i = 0; $i<$num_vlans; $i++) {
      while (1) {
	my $vid = $starting_vid + $i;
	$utils->updatePort($p1, $shelf, $lf1, "$pname\.$vid");
	if ($lf2 ne "") {
	  $vid = $starting_vid + $num_vlans + $i;
	  $utils->updatePort($p2, $shelf, $lf2, "$pname2\.$vid");
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
}#add8021qVlans


# Wait untill the system can update a port..
sub throttleCard {
  my $s = shift;
  my $c = shift;
  my $p1 = new LANforge::Port();
  $utils->updatePort($p1, $s, $c, 1);
}#throttle

sub initPortsToDefault {
  clearVlanPorts($shelf, $lf1);
  if ($lf2 ne "") {
    clearVlanPorts($shelf, $lf2);
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

sub clearVlanPorts {
  my $s = shift;
  my $c = shift;

  my $i;
  my $found_one = 1;
  my @ports = ();
  while ($found_one) {
    $found_one = 0;
    doCmd("probe_ports");
    # Clear out any existing VLAN ports.
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
      my $tst = $ports[$i]->is8021qVlan();
      if ($use_mac_vlans) {
	$tst = $ports[$i]->isMacVlan();
      }
      if ($tst) {
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
              "172.29.0.5 NA NA NA";
    doCmd($cmd);
    $ip_lsb++;

    if ($lf2 ne "") {
      $cmd = "set_port $shelf $lf2 $tmp2 $ip_base.$ip_c.$ip_lsb $msk " .
	"172.29.0.5 NA NA NA";
      doCmd($cmd);
      $ip_lsb++;
    }

    my $p1 = new LANforge::Port();
    $utils->updatePort($p1, $shelf, $lf1, $tmp);
    my $pname = $p1->{dev};

    my $q;
    my $throttle = 25;
    my $since_throttle = 0;
    for ($q = 0; $q<$num_vlans; $q++) {
      my $vid = $starting_vid + $q;
      my $pnm = "$pname\.$vid";
      if ($use_mac_vlans) {
	$pnm = "$pname\#$q";
      }
      $cmd = "set_port $shelf $lf1 $pnm $ip_base.$ip_c.$ip_lsb $msk " .
	     "172.29.0.5 NA NA NA";
      doCmd($cmd);
      $ip_lsb++;

      if ($ip_lsb > 250) {
	$ip_c++;
	$ip_lsb = 2;
      }

      if ($since_throttle++ > $throttle) {
	my $p1 = new LANforge::Port();
	$utils->updatePort($p1, $shelf, $lf1, "$pnm");
	$since_throttle = 0;
      }

    }

    $ip_lsb++;

    if ($lf2 ne "") {
      $p1 = new LANforge::Port();
      $utils->updatePort($p1, $shelf, $lf2, $tmp2);
      $pname = $p1->{dev};

      for ($q = 0; $q<$num_vlans; $q++) {
	my $vid = $starting_vid + $num_vlans + $q;
	my $pnm = "$pname\.$vid";
	if ($use_mac_vlans) {
	  $pnm = "$pname\#$q";
	}
	$cmd = "set_port $shelf $lf2 $pnm $ip_base.$ip_c.$ip_lsb $msk " .
	  "172.29.0.5 NA NA NA";
	doCmd($cmd);
	$ip_lsb++;

	if ($ip_lsb > 250) {
	  $ip_c++;
	  $ip_lsb = 2;
	}

	if ($since_throttle++ > $throttle) {
	  my $p1 = new LANforge::Port();
	  $utils->updatePort($p1, $shelf, $lf2, "$pnm");
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
    for ($q = 0; $q<$num_vlans; $q++) {
      if ($use_mac_vlans) {
	@all_ports1 = (@all_ports1, "$pname\#$q");
      }
      else {
	my $vid = $starting_vid + $q;
	@all_ports1 = (@all_ports1, "$pname\.$vid");
      }
    }
  }

  my @all_ports2 = @lf2_ports;
  if ($lf2 ne "") {
    for ($j = 0; $j<@lf2_ports; $j++) {
      my $p1 = new LANforge::Port();
      $utils->updatePort($p1, $shelf, $lf2, $lf2_ports[$j]);
      $pname = $p1->{dev};

      my $q;
      for ($q = 0; $q<$num_vlans; $q++) {
	if ($use_mac_vlans) {
	  @all_ports2 = (@all_ports2, "$pname\#$q");
	}
	else {
	  my $vid = $starting_vid + $num_vlans + $q;
	  @all_ports2 = (@all_ports2, "$pname\.$vid");
	}
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

	my $ep1 = "l4-${num[$ep]}-TX";
	$ep++;
	my $ep2 = "D_l4-${num[$ep]}-TX";
	$ep++;

	@endpoint_names = (@endpoint_names, $ep1, $ep2);

	# Add the dummy endpoint
	my $cmd = "add_l4_endp $ep2 $shelf $lf1 " . $all_ports1[$j] . " l4_generic  0 0 0 ' ' ' '";
	doCmd($cmd);
	$cmd = "set_endp_flag $ep2 unmanaged 1";
	doCmd($cmd);

	my $save_file = "/tmp/$ep1";
	if ($save_to_dev_null) {
	  $save_file = "/dev/null";
	}
	$cmd = "add_l4_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " l4_generic 0 10000 $url_per_10m '" .
	  "dl $l4_url $save_file' ' '";
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

	my $ep1 = "endp-${num[$ep]}-TX";
	$ep++;
	my $ep2 = "endp-${num[$ep]}-RX";
	$ep++;

	@endpoint_names = (@endpoint_names, $ep1, $ep2);

	my $cmd = "add_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " " . @cx_types[$i] .
	    " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " . $max_pkt_szs[$i] .
	    " $pattern NO";
	doCmd($cmd);


	if ($lf2 == "") {
	  die("Must lave lf2 defined if using non-l4 endpoints.");
	}

	$cmd =    "add_endp $ep2 $shelf $lf2 " . $all_ports2[$j] . " " . @cx_types[$i] .
	    " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " .
	    $max_pkt_szs[$i] . " $pattern NO";
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

	  my $ep1 = "l4-${num[$ep]}-TX";
	  $ep++;
	  my $ep2 = "D_l4-${num[$ep]}-TX";
	  $ep++;

	  @endpoint_names = (@endpoint_names, $ep1, $ep2);

	  # Add the dummy endpoint
	  my $cmd = "add_l4_endp $ep2 $shelf $lf1 " . $all_ports1[$j] . " l4_generic  0 0 0 ' ' ' '";
	  doCmd($cmd);
	  $cmd = "set_endp_flag $ep2 unmanaged 1";
	  doCmd($cmd);

	  my $save_file = "/tmp/$ep1";
	  if ($save_to_dev_null) {
	    $save_file = "/dev/null";
	  }
	  $cmd = "add_l4_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " l4_generic 0 10000 $url_per_10m '" .
	       "dl $l4_url $save_file' ' '";
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

	  my $ep1 = "endp-${num[$ep]}-TX";
	  $ep++;
	  my $ep2 = "endp-${num[$ep]}-RX";
	  $ep++;

	  @endpoint_names = (@endpoint_names, $ep1, $ep2);

	  my $cmd = "add_endp $ep1 $shelf $lf1 " . $all_ports1[$j] . " " . @cx_types[$i] .
	    " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " . $max_pkt_szs[$i] .
	      " $pattern NO";
	  doCmd($cmd);

	  if ($lf2 == "") {
	    die("Must lave lf2 defined if using non-l4 endpoints.");
	  }

	  $cmd =    "add_endp $ep2 $shelf $lf2 " . $all_ports2[$j] . " " . @cx_types[$i] .
	    " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " .
	      $max_pkt_szs[$i] . " $pattern NO";
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


sub doCmd {
  my $cmd = shift;

  print ">>> $cmd\n";

  $t->print($cmd);
  my @rslt = $t->waitfor('/ \>\>RSLT:(.*)/');
  print "**************\n @rslt ................\n\n";
  #sleep(1);
}
