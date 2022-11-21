#!/usr/bin/perl

# This program is used to verify LANforge configuration sub-systems.
# It uses the LANforge::Endpoint perl module to parse output from
# the CLI.

# This script sets up connections of types:
#   lf, lf_udp, lf_tcp, custom_ether, custom_udp, and custom_tcp
# across 3 ports on 2 machines.
# It then changes values and checks to see if the values set correctly.

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

# This sets up connections between 2 LANforge machines
my $lf1 = 1;
my $lf2 = 2;

# Port pairs.  These are the ports that should be talking to each other.
# Ie, the third column in lf1_ports talks to the third column in lf2_ports.
my @lf1_ports = ("wlan0");
my @lf2_ports = ("vap0000");

my $ports_are_connected = 0; # Connected to each other.  If true, we can test some
                             # ethernet driver settings more precisely.

my $manual_check = 0; # If this is true, then user input will be asked for each time
                      # there is a test failure.  Good for manually checking the script, etc.

my $ip_base = "172.1";

# Set up one CX of each of these types on each port pair.
my @cx_types =     ("lf", "lf_udp", "lf_tcp", "custom_udp", "custom_tcp");
my @min_pkt_szs =  (64,   20,       20,        1,            1);
my @max_pkt_szs =  (1514, 65507,    65535,     2048,         2048);

my $min_rate = 0;
my $max_rate = 1024000;

my $test_mgr = "ben_tm";

my $report_timer = 3000; # 3 seconds


########################################################################
# Nothing to configure below here, most likely.
########################################################################
my $usage = "$0  [--host {lanforge-mgr-host}]

Example:
 $0 --host localhost\n";

my $i = 0;

GetOptions 
(
	'host|h=s'		=> \$lfmgr_host,
) || die("$usage");


my @endpoint_names = (); #will be added to as they are created
my @cx_names = ();

my $fail_msg = "";

# Configure our utils.
our $utils = new LANforge::Utils();
$::utils->connect($lfmgr_host, $lfmgr_port);
$utils->cli_send_silent(0); # Do show input to CLI
$utils->cli_rcv_silent(0);  # Repress output from CLI ??


my $dt = "";

# Do discovery to make sure the server knows about all servers.  Good for when
# you just restarted all the servers and want to run the test real fast now!
$utils->doCmd("discover");
sleep(2);
$utils->doCmd("discover");
sleep(2);


initToDefaults();

print "Sleeping 3 seconds to let port initialization complete.\n";
sleep(3); # Let everything settle down a bit...

# Now, add back the test manager we will be using
$utils->doCmd("add_tm $test_mgr");
$utils->doCmd("tm_register $test_mgr default");  #Add default user
$utils->doCmd("tm_register $test_mgr default_gui");  #Add default GUI user

# $utils->doCmd("log_level 63");

# Change all kinds of things on the ports, they should end up configured
# and ready for endpoints to be added.
testPortModification();

testCxModification();

$dt = `date`;
chomp($dt);
print "\n\n\nCompleted at: $dt\n\n";

if (length($fail_msg) > 0) {
  print "Some sub-tests failed:\n$fail_msg\n";
}
else {
  print "All tests passed successfully.\n";
}

exit(0);


sub initToDefaults {
  # Clean up database if stuff exists

  $utils->doCmd("rm_cx $test_mgr all");
  $utils->doCmd("rm_endp YES_ALL");
  $utils->doCmd("rm_test_mgr $test_mgr");

  initPortsToDefault();
}#initToDefaults


sub initPortsToDefault {
  # Set all ports we are messing with to known state.
  my $i = 0;
  for ($i = 0; $i<@lf1_ports; $i++) {
    my $tmp = $lf1_ports[$i];
    my $tmp2 = $lf2_ports[$i];
    $utils->doCmd("set_port $shelf_num $lf1 $tmp 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
    $utils->doCmd("set_port $shelf_num $lf2 $tmp2 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
  }
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
  }
}#testFailed

sub testPortModification {
  # Set all ports we are messing with to known state.
  my $i = 0;
  for ($i = 0; $i<@lf1_ports; $i++) {
    my $tmp = $lf1_ports[$i];
    my $tmp2 = $lf2_ports[$i];
    my $tmp_ip = $i + 2;
    my $tmp_ip2 = $i + 102;

    my $cmd = "set_port $shelf_num $lf1 $tmp $ip_base.1.$tmp_ip 255.255.255.0 $ip_base.1.1 NA NA NA";
    $utils->doCmd($cmd);
    sleep(1);

    my $p1 = new LANforge::Port();

    # Tell the port what it is so it decodes the right one..
    $utils->updatePort($p1, $shelf_num, $lf1, $tmp);

    verifyPortAttributes($p1, $shelf_num, $lf1, $tmp, "$ip_base.1.$tmp_ip", "255.255.255.0",
			 "$ip_base.1.1");
    testMacSettability($p1);
    testMtuSettability($p1);
    testQlenSettability($p1);

    $cmd = "set_port $shelf_num $lf2 $tmp2 $ip_base.1.$tmp_ip2 255.255.255.0 $ip_base.1.1 NA NA NA";
    $utils->doCmd($cmd);

    my $p2 = new LANforge::Port();

    # Tell the port what it is so it decodes the right one..
    $utils->updatePort($p2, $shelf_num, $lf2, $tmp2);

    verifyPortAttributes($p2, $shelf_num, $lf2, $tmp2, "$ip_base.1.$tmp_ip2", "255.255.255.0",
			 "$ip_base.1.1");

    testMacSettability($p2);
    testMtuSettability($p2);
    testQlenSettability($p2);

    testRateSettability($p1, $p2);

  }
}#testPortModification


sub testCxModification {
  my $ep = 0;
  my $cx = 0;
  my $i = 0;

  for ($i = 0; $i<@cx_types; $i++) {
    my $j = 0;
    for ($j = 0; $j<@lf1_ports; $j++) {
      my $burst = "NO";
      if ($min_rate != $max_rate) {
	$burst = "YES";
      }
      my $szrnd = "NO";
      if ($min_pkt_szs[$i] != $max_pkt_szs[$i]) {
	$szrnd = "YES";
      }
      my $pattern = "INCREASING";
      if ($cx_types[$i] =~ /custom/) {
	$pattern = "CUSTOM";
      }

      my $ep1 = "endp-${ep}-TX";
      $ep++;
      my $ep2 = "endp-${ep}-RX";
      $ep++;

      @endpoint_names = (@endpoint_names, $ep1, $ep2);

      my $cmd = "add_endp $ep1 $shelf_num $lf1 " . $lf1_ports[$j] . " " . $cx_types[$i] .
                " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " . $max_pkt_szs[$i] .
                " $pattern NO";
      $utils->doCmd($cmd);

      my $endp1 = new LANforge::Endpoint();
      $utils->updateEndpoint($endp1, $ep1);
      verifyEndpointAttributes($endp1, $ep1, $shelf_num, $lf1, $lf1_ports[$j], $cx_types[$i], -1, $burst,
			       $min_rate, $max_rate, $szrnd, $min_pkt_szs[$i], $max_pkt_szs[$i], $pattern,
			       "NO"); # last is use_checksum
      testEndpointSettability($endp1);


      $cmd =    "add_endp $ep2 $shelf_num $lf2 " . $lf2_ports[$j] . " " . @cx_types[$i] .
                " -1 $burst $min_rate $max_rate $szrnd " . $min_pkt_szs[$i] . " " .
		$max_pkt_szs[$i] . " $pattern NO";

      $utils->doCmd($cmd);

      my $endp2 = new LANforge::Endpoint();
      $utils->updateEndpoint($endp2, $ep2);
      verifyEndpointAttributes($endp2, $ep2, $shelf_num, $lf2, $lf2_ports[$j], $cx_types[$i], -1, $burst,
			       $min_rate, $max_rate, $szrnd, $min_pkt_szs[$i], $max_pkt_szs[$i], $pattern,
			       "NO"); # last is use_checksum
      testEndpointSettability($endp2);

      # Now, add the cross-connects
      my $cx_name = "cx-${cx}";
      $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
      $utils->doCmd($cmd);
      $utils->doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");

      $cx++;

      @cx_names = (@cx_names, $cx_name);

    }#for all ports
  }#for all endpoint types
}#addCrossConnects


sub testQlenSettability {
  my $p1 = shift;
  testQlenSettabilityHelper($p1, "100");
  testQlenSettabilityHelper($p1, "800");
  testQlenSettabilityHelper($p1, "400");
}#testQlenSettability

sub testMtuSettability {
  my $p1 = shift;
  testMtuSettabilityHelper($p1, "1500");
  testMtuSettabilityHelper($p1, "1400");
  testMtuSettabilityHelper($p1, "1496");

  # It is not un-usual for these to fail
  testMtuSettabilityHelper($p1, "1504");
  testMtuSettabilityHelper($p1, "4096");
  testMtuSettabilityHelper($p1, "8192");

  # This should work, set it back to defaults.
  testMtuSettabilityHelper($p1, "1500");
}#testMtuSettability


sub testMtuSettabilityHelper {
  my $p1 = shift;
  my $mtu = shift;

  $p1->mtu($mtu);
  my $cmd = $p1->getSetMtuCmd();
  $utils->doCmd($cmd);
  $utils->updatePort($p1);
  my $p = $p1->toStringBrief();

  if ($p1->mtu() ne $mtu) {
    # Give one more chance for things to be right, maybe the driver is slow...
    print ("   *** WARNING: $p: Failed to set MTU correctly, tried: $mtu  got: " .
	   $p1->mtu() . "\n         Going to wait 2 seconds and update the port again..\n");
    sleep(2);
    $utils->updatePort($p1);
  }

  ($p1->mtu() eq $mtu) or testFailed("$p: Failed to set MTU correctly, tried: $mtu  got: " .
				     $p1->mtu() . "\n");
}#testMtuSettability

sub testQlenSettabilityHelper {
  my $p1 = shift;
  my $val = shift;

  $p1->tx_q_len($val);
  my $cmd = $p1->getSetTxQueueLenCmd();
  $utils->doCmd($cmd);
  $utils->updatePort($p1);
  my $p = $p1->toStringBrief();

  if ($p1->tx_q_len() ne $val) {
    # Give one more chance for things to be right, maybe the driver is slow...
    print ("   *** WARNING: $p: Failed to set Tx-Queue-Length correctly, tried: $val  got: " .
	   $p1->tx_q_len() . "\n         Going to wait 2 seconds and update the port again..\n");
    sleep(2);
    $utils->updatePort($p1);
  }

  $p1->tx_q_len() eq $val or testFailed("$p: Failed to set Tx-Queue-Length correctly, tried: $val  got: " .
					 $p1->tx_q_len() . "\n");
}


sub testRateSettability {
  my $p1 = shift;
  my $p2 = shift;

  testSolitaryPortSettability($p1);
  testSolitaryPortSettability($p2);

  if ($ports_are_connected) {
    # TODO:  Test partner flags
  }
}#testRateSettability


sub testSolitaryPortSettability {
  my $p1 = shift;

  my $gbfd = "";
  my $gbhd = "";
  my $fc = "";
  if ($p1->supported_flags() =~ /1000bt/) {
    $gbfd = " 1000bt-FD";
    $gbhd = " 1000bt-HD";
  }

  if ($p1->supported_flags() =~ /FLOW-CONTROL/) {
    $fc = " FLOW-CONTROL";
  }

  advertTestHelper($p1, "10bt-HD 10bt-FD 100bt-HD 100bt-FD" . $gbhd . $gbfd . $fc);
  advertTestHelper($p1, "10bt-HD 10bt-FD 100bt-HD 100bt-FD" . $fc);
  advertTestHelper($p1, "10bt-HD 10bt-FD 100bt-HD 100bt-FD");
  advertTestHelper($p1, "10bt-HD 10bt-FD 100bt-HD");
  advertTestHelper($p1, "10bt-HD 10bt-FD");
  advertTestHelper($p1, "10bt-HD");
  advertTestHelper($p1, "100bt-FD");
  advertTestHelper($p1, "100bt-HD");
  advertTestHelper($p1, "10bt-FD");
  advertTestHelper($p1, "10bt-HD");
  advertTestHelper($p1, "10bt-HD 10bt-FD 100bt-HD 100bt-FD" . $gbhd . $gbfd . $fc);

  if ($gbfd ne "") {
    fixedTestHelper($p1, "1000bt-FD");
    fixedTestHelper($p1, "1000bt-HD");
  }
  fixedTestHelper($p1, "100bt-FD");
  fixedTestHelper($p1, "100bt-HD");
  fixedTestHelper($p1, "10bt-FD");
  fixedTestHelper($p1, "10bt-HD");

  advertTestHelper($p1, "10bt-HD 10bt-FD 100bt-HD 100bt-FD" . $gbhd . $gbfd . $fc);
}#testSolitaryPortSettability


sub fixedTestHelper {
  my $p1 = shift;
  my $adv = shift;

  $p1->setRate($adv);
  my $cmd = $p1->getSetRateCmd();
  $utils->doCmd($cmd);
  sleep(2); # Give the hardware a chance to do what it needs.
  $utils->updatePort($p1);

  if (!$p1->isCurrent($adv)) {
    # Give one more chance for things to be right, maybe the driver is slow...
    print ("   *** WARNING: $p: Failed to set fixed rate correctly, tried: $adv  got: " .
	   $p1->cur_flags() . "\n         Going to wait 2 seconds and update the port again..\n");
    sleep(2);
    $utils->updatePort($p1);
  }

  my $p = $p1->toStringBrief();
  $p1->isCurrent($adv) or testFailed("$p: Failed to set fixed rate correctly, tried: $adv  got: " .
				     $p1->cur_flags() . "\n");
}#fixedTestHelper


sub advertTestHelper {
  my $p1 = shift;
  my $adv = shift;

  $p1->setRate("auto");
  $p1->advert_flags("$adv");
  my $cmd = $p1->getSetRateCmd();
  $utils->doCmd($cmd);
  $utils->updatePort($p1);
  my $p = $p1->toStringBrief();
  $p1->isAdvertising($adv) or testFailed("$p: Failed to set advertise rates correctly, tried: $adv  got: " .
					 $p1->advert_flags() . "\n");
}#advertTestHelper


sub testMacSettability {
  my $port = shift;

  # Get & save the original MAC
  my $mac = $port->mac_addr();
  my $sn = $port->shelf_id();
  my $cn = $port->card_id();
  my $pn = $port->port_id();

  my $new_mac = "00:11:22:$sn$sn:$cn$cn:$pn$pn";
  $port->mac_addr($new_mac);
  $cmd = $port->getSetCmd();
  $utils->doCmd($cmd);
  $utils->updatePort($port);
  my $p = $port->toStringBrief();
  $port->mac_addr() eq $new_mac or testFailed("$p: Could not set MAC addr, current: " . $port->mac_addr()
					      . " desired: $new_mac\n");
  # Set it back to original value
  $port->mac_addr($mac);
  $cmd = $port->getSetCmd();
  $utils->doCmd($cmd);
  $utils->updatePort($port);
  $p = $port->toStringBrief();
  $port->mac_addr() eq $mac or testFailed("$p: Could not set MAC addr, current: " . $port->mac_addr()
					  . " desired: $mac\n");

  print "Setting MAC for Port $sn.$cn.$pn verified as correct!\n";

}#testMacSettability


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
  my $tos = shift;
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

  if (defined($tos)) {
    $endp->ip_tos() eq $tos or testFailed("$p: ToS: " . $endp->ip_tos() .
					  " does not match: $tos\n", $should_fail);
  }

}#verifyEndpointAttributes


sub testEndpointSettability {
  my $endp = shift;

  print "\n*****\n >>Testing " . $endp->toStringBrief() . " rate settability.\n";

  # Test setting the rates
  testEndpRateSet($endp, 0, 0, "NO");
  testEndpRateSet($endp, 2000, 2000, "NO");
  testEndpRateSet($endp, 0, 10000000, "YES");
  testEndpRateSet($endp, 65000, 128000, "YES");
  testEndpRateSet($endp, 512000, 1024000, "YES");
  testEndpRateSet($endp, 1024000, 512000, "NO", "YES"); # Should fail
  testEndpRateSet($endp, 512000, 1024000, "YES");

  if ($endp->usesIP()) {
    testEndpTosSet($endp, 0x01, "YES");
    testEndpTosSet($endp, 0x02, "NO");
    testEndpTosSet($endp, 0x04, "YES");
    testEndpTosSet($endp, 0x06, "NO");
    testEndpTosSet($endp, 0x0a, "NO");
    testEndpTosSet($endp, 0x12, "NO");
    testEndpTosSet($endp, 0x02, "NO");
    testEndpTosSet($endp, "DONT-SET", "NO");
  }

  # Test payload & payload size changes
  if ($endp->isCustom()) {
    testEndpPldSet($endp);
  }
  else {
    testEndpPldSizeSet($endp, 67, 1457, "YES");
    testEndpPldSizeSet($endp, 500, 457, "YES", "YES"); # should fail
    testEndpPldSizeSet($endp, 500, 500, "NO");
    testEndpPldSizeSet($endp, -1, 70000000, "YES", "YES"); #should fail
    testEndpPldSizeSet($endp, 128, 1500, "YES");
  }

  # TODO: Change & check stuff
}#testEndpointSettability


sub testEndpPldSet {
  my $endp = shift;

  my $pld = "00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff";

  testEndpPldSetHelper($endp, $pld);

  $pld = genRandomHex(2048);
  if ($endp->ep_type() =~ /CUSTOM_ETHER/) {
    testEndpPldSetHelper($endp, $pld, "YES"); # Should fail
  }
  else {
    testEndpPldSetHelper($endp, $pld, "NO"); #Shouldn't fail
  }

  $pld = genRandomHex(17);
  if ($endp->ep_type() =~ /CUSTOM_ETHER/) {   # Too short for ethernet, should fail.
    testEndpPldSetHelper($endp, $pld, "YES");
  }
  else {
    testEndpPldSetHelper($endp, $pld, "NO");
  }
  $pld = genRandomHex(1000);
  testEndpPldSetHelper($endp, $pld);

  $pld = genRandomHex(2049);
  testEndpPldSetHelper($endp, $pld, "YES"); # Payload is too long, only support 2000 bytes at this time.

  $pld = "00 11 22 gg 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff";

  testEndpPldSetHelper($endp, $pld, "YES");  # Should fail, has 'gg' in it, which is not hex!

  $pld = "zz 11 22 gg 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff";

  testEndpPldSetHelper($endp, $pld, "YES");  # Should fail, has 'zz' in it, which is not hex!

  $pld = "00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee ff 00 11 22 33 44 55 66 77 88 99 aa bb cc dd ee zz";

  testEndpPldSetHelper($endp, $pld, "YES");  # Should fail, has 'zz' in it, which is not hex!

  $pld = genRandomHex(1000);
  testEndpPldSetHelper($endp, $pld);

}#testEndpPldSet

sub testEndpPldSetHelper {
  my $endp = shift;
  my $pld = shift;
  my $should_fail = shift;

  $endp->payload($pld);

  my $cmd = $endp->getSetPayloadCmd();
  $utils->doCmd($cmd);

  $utils->updateEndpoint($endp);

  my $p = $endp->toStringBrief();
  if ($endp->payload() ne $pld) {
    if (defined($should_fail) && ($should_fail eq "YES")) {
      # This is very verbose if the payload is printed out, so not going to print it all here,
      # but just the lengths instead.  This is also expected behaviour (notice the should_fail == YES).
      testFailed("$p: Payload does not match, lengths: " . length($endp->payload()) . " "
		 . length($pld) . "\n", $should_fail);
    }
    else {
      testFailed("$p: Payload:\n-:" . $endp->payload() . ":- does not match:\n-:$pld:-\n", $should_fail);
    }
  }
  else {
    if (defined($should_fail) && ($should_fail eq "YES")) {
      testFailed("$p: Payload:\n-:" . $endp->payload() . ":- does match (and should have failed)\n");
    }
  }
}#testEndpPldSetHelper


sub testEndpPldSizeSet {
  my $endp = shift;
  my $min = shift;
  my $max = shift;
  my $rand = shift;
  my $should_fail = shift;

  my $en = $endp->name();
  my $sn = $endp->shelf_id();
  my $cn = $endp->card_id();
  my $pn = $endp->port_id();
  my $et = $endp->ep_type();
  my $ipp = $endp->ip_port();
  my $minrt = $endp->min_tx_rate();
  my $mxrt = $endp->max_tx_rate();
  my $pt = $endp->pattern();
  my $cs = $endp->checksum();
  my $burst = $endp->getBursty();
  my $tos = $endp->ip_tos();

  $endp->min_pkt_size($min);
  $endp->max_pkt_size($max);
  $endp->setRandom($rand);

  my @cmds = $endp->getSetCmds();
  my $i;
  for ($i = 0; $i<@cmds; $i++) {
    $utils->doCmd($cmds[$i]);
  }

  $utils->updateEndpoint($endp);

  verifyEndpointAttributes($endp, $en, $sn, $cn, $pn, $et, $ipp, $burst, $minrt, $mxrt, $rand,
			   $min, $max, $pt, $cs, $tos, $should_fail);
}#testEndpPldSizeSet


sub testEndpRateSet {
  my $endp = shift;
  my $min = shift;
  my $max = shift;
  my $burst = shift;
  my $should_fail = shift;

  my $en = $endp->name();
  my $sn = $endp->shelf_id();
  my $cn = $endp->card_id();
  my $pn = $endp->port_id();
  my $et = $endp->ep_type();
  my $ipp = $endp->ip_port();
  my $tos = $endp->ip_tos();

  my $sr = $endp->size_random();
  my $minpkt = $endp->min_pkt_size();
  my $mxpkt = $endp->max_pkt_size();
  my $pt = $endp->pattern();
  my $cs = $endp->checksum();

  $endp->min_tx_rate($min);
  $endp->max_tx_rate($max);
  $endp->setBursty($burst);

  my @cmds = $endp->getSetCmds();
  my $i;
  for ($i = 0; $i<@cmds; $i++) {
    $utils->doCmd($cmds[$i]);
  }

  $utils->updateEndpoint($endp);

  verifyEndpointAttributes($endp, $en, $sn, $cn, $pn, $et, $ipp, $burst, $min, $max, $sr,
			   $minpkt, $mxpkt, $pt, $cs, $tos, $should_fail);

}#testEndpRateSet


sub testEndpTosSet {
  my $endp = shift;
  my $tos = shift;
  my $should_fail = shift;

  my $en = $endp->name();
  my $sn = $endp->shelf_id();
  my $cn = $endp->card_id();
  my $pn = $endp->port_id();
  my $et = $endp->ep_type();
  my $ipp = $endp->ip_port();

  my $sr = $endp->size_random();
  my $minpkt = $endp->min_pkt_size();
  my $mxpkt = $endp->max_pkt_size();
  my $pt = $endp->pattern();
  my $cs = $endp->checksum();

  $endp->ip_tos($tos);

  my @cmds = $endp->getSetCmds();
  my $i;
  for ($i = 0; $i<@cmds; $i++) {
    $utils->doCmd($cmds[$i]);
  }

  $utils->updateEndpoint($endp);

  verifyEndpointAttributes($endp, $en, $sn, $cn, $pn, $et, $ipp, $burst, $min, $max, $sr,
			   $minpkt, $mxpkt, $pt, $cs, $tos, $should_fail);

}#testEndpTosSet


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
