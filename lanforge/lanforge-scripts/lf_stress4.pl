#!/usr/bin/perl

# This program is used to stress test the LANforge system, and may be used as
# an example for others who wish to automate LANforge tests.

# This specifically is designed for two machines with 3 data-generating ports each.

# Un-buffer output
$| = 1;

use Net::Telnet ();

my $lfmgr_host = "localhost";
my $lfmgr_port = 4001;

my $shelf_num = 1;

# Specify 'card' numbers for this configuration.
my $lanf1 = 1;
my $lanf2 = 2;

my $test_mgr = "ben_tm";

my $loop_max = 100;
my $start_stop_iterations = 100;
my $run_for_time = (60 * 60 * 24);  # Run for XX seconds..then will be stopped again
my $stop_for_time = 5;  # Stop for XX seconds..then will be started again
my $report_timer = 3000; # 3 seconds


########################################################################
# Nothing to configure below here, most likely.
########################################################################

my @endpoint_names = (); #will be added to as they are created
my @cx_names = ();

# Open connection to the LANforge server.

my $t = new Net::Telnet(Prompt => '/default\@btbits\>\>/');


$t->open(Host    => $lfmgr_host,
	 Port    => $lfmgr_port,
	 Timeout => 10);

$t->waitfor("/btbits\>\>/");

my $dt = "";

# Do some thing over and over again...
my $loops = 0;
for ($loop = 0; $loop<$loop_max; $loop++) {
  $dt = `date`;
  chomp($dt);
  print "\n\n*****  Starting loop: $loop at: $dt  *****\n\n";

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

  # Add our endpoints
  addCrossConnects();

  my $rl = 0;
  for ($rl = 0; $rl<$start_stop_iterations; $rl++) {
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


sub initPortsToDefault {
  # Set all ports we are messing with to known state.
  my $i = 0;

  # All have 3 ports
  for ($i = 1; $i<=3; $i++) {
    doCmd("set_port $shelf_num $lanf1 $i 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
    doCmd("set_port $shelf_num $lanf2 $i 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
  }
}


sub initIpAddresses {
  # Set all ports we are messing with to known state.

  # Syntax for setting port info is:
  # set_port [shelf] [card] [port] [ip] [mask] [gateway] [cmd-flags] [cur-flags] [MAC]
  # NOTE:  Just use NA for the flags for now...not tested otherwise.

  # Set up the 3 10/100 ports.  They will be set up to talk to
  # each other.
  doCmd("set_port $shelf_num $lanf1 1 172.25.7.2 255.255.255.0 172.25.7.1 NA NA NA");
  doCmd("set_port $shelf_num $lanf1 2 172.25.8.2 255.255.255.0 172.25.8.1 NA NA NA");
  doCmd("set_port $shelf_num $lanf1 3 172.25.8.4 255.255.255.0 172.25.8.1 NA NA NA");
  doCmd("set_port $shelf_num $lanf2 1 172.25.7.4 255.255.255.0 172.25.7.1 NA NA NA");
  doCmd("set_port $shelf_num $lanf2 2 172.25.8.3 255.255.255.0 172.25.8.1 NA NA NA");
  doCmd("set_port $shelf_num $lanf2 3 172.25.8.5 255.255.255.0 172.25.8.1 NA NA NA");


}

sub addCrossConnects {
  # Syntax for adding an endpoint is:
  # add_endp [alias] [shelf] [card] [port] [type] [IP-port] [bursty] [min_rate] [max_rate]
  #          [pkt_sz_random] [min_pkt] [max_pkt] [pattern] [use_checksum]

  # Set up 3 TCP cross-connects between lanf1 and lanf2
  my $i = 1;
  my $tp = "tcp";
  my $tp2 = "lf_tcp";
  my $rate = 6000000; # 6Mbps

  for ($i = 1; $i<=3; $i++) {
    my $tx_nm = "${tp}-qp${i}-TX";
    my $rx_nm = "${tp}-qp${i}-RX";

    doCmd("add_endp $tx_nm $shelf_num $lanf1 $i $tp2 -1 NO $rate $rate NO 4000 4000 random_fixed NO");

    my $rt = $rate / 2; # Non-symetric cross-connect

    doCmd("add_endp $rx_nm $shelf_num $lanf2 $i $tp2 -1 NO $rt $rt NO 4000 4000 decreasing NO");

    my $cx_nm = "${tp}-qp${i}";
    # Add cross-connect
    doCmd("add_cx $cx_nm $test_mgr $tx_nm $rx_nm");

    @endpoint_names = (@endpoint_names, $rx_nm, $tx_nm);
    @cx_names = (@cx_names, $cx_nm);
  }


  # Set up 3 UDP cross-connects between lanf1 and lanf2
  my $i = 1;
  my $tp = "udp";
  my $tp2 = "lf_udp";
  my $rate = 6000000; # 6Mbps

  for ($i = 1; $i<=3; $i++) {
    my $tx_nm = "${tp}-qp${i}-TX";
    my $rx_nm = "${tp}-qp${i}-RX";

    doCmd("add_endp $tx_nm $shelf_num $lanf2 $i $tp2 -1 NO $rate $rate NO 4000 4000 random_fixed NO");

    my $rt = $rate / 2; # Non-symetric cross-connect

    doCmd("add_endp $rx_nm $shelf_num $lanf1 $i $tp2 -1 NO $rt $rt NO 4000 4000 decreasing NO");

    my $cx_nm = "${tp}-qp${i}";
    # Add cross-connect
    doCmd("add_cx $cx_nm $test_mgr $tx_nm $rx_nm");

    @endpoint_names = (@endpoint_names, $rx_nm, $tx_nm);
    @cx_names = (@cx_names, $cx_nm);
  }

}#addCrossConnects


sub doCmd {
  my $cmd = shift;

  print ">>> $cmd\n";

  $t->print($cmd);
  my @rslt = $t->waitfor('/ \>\>RSLT:(.*)/');
  print "**************\n @rslt ................\n\n";
  #sleep(1);
}
