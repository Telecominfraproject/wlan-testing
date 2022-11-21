#!/usr/bin/perl

# This program is used to stress test the LANforge system, and may be used as
# an example for others who wish to automate LANforge tests.

# This script sets up connections of types:
#   lf, lf_udp, lf_tcp, custom_ether, custom_udp, and custom_tcp
# across 3 ports on 2 machines.
# It then continously starts and stops the connections.

# Un-buffer output
$| = 1;

use Net::Telnet ();

my $lfmgr_host = "localhost";
my $lfmgr_port = 4001;

my $shelf_num = 1;

# This sets up connections between 2 LANforge machines
my $lf1 = 1;
my $lf2 = 2;

# Port pairs.  These are the ports that should be talking to each other.
# Ie, the third column in lf1_ports talks to the third column in lf2_ports.
my @lf1_ports = ( 1, 2, 3 );
my @lf2_ports = ( 1, 2, 3 );

my @lf1_port_ips = ( "172.1.1.2", "172.1.2.2", "172.1.2.200" );
my @lf2_port_ips = ( "172.1.1.3", "172.1.2.3", "172.1.2.201" );

my @lf1_port_gws = ( "172.1.1.1", "172.1.2.1", "172.1.2.1" );
my @lf2_port_gws = ( "172.1.1.1", "172.1.2.1", "172.1.2.1" );

# Set up one CX of each of these types on each port pair.
my @cx_types =
  ( "lf", "lf_udp", "lf_tcp", "custom_ether", "custom_udp", "custom_tcp" );
my @min_pkt_szs = ( 64,   1,     1,     64,   1,    1 );
my @max_pkt_szs = ( 1514, 12000, 13000, 1514, 2048, 2048 );

my $min_rate = 512000;
my $max_rate = 1024000;

my $test_mgr = "ben_tm";

my $loop_max              = 100;
my $start_stop_iterations = 100;
my $run_for_time  = 120;     # Run for XX seconds..then will be stopped again
my $stop_for_time = 5;       # Run for XX seconds..then will be stopped again
my $report_timer  = 3000;    # 3 seconds

########################################################################
# Nothing to configure below here, most likely.
########################################################################

my @endpoint_names = ();     #will be added to as they are created
my @cx_names       = ();

# Open connection to the LANforge server.

my $t = new Net::Telnet( Prompt => '/default\@btbits\>\>/' );

$t->open(
   Host    => $lfmgr_host,
   Port    => $lfmgr_port,
   Timeout => 10
);

$t->waitfor("/btbits\>\>/");

my $dt = "";

my $loops = 0;
for ( $loop = 0 ; $loop < $loop_max ; $loop++ ) {
   $dt = `date`;
   chomp($dt);
   print "\n\n*****  Starting loop: $loop at: $dt  *****\n\n";

   initToDefaults();

   #exit(0);

   # Now, add back the test manager we will be using
   doCmd("add_tm $test_mgr");
   doCmd("tm_register $test_mgr default");        #Add default user
   doCmd("tm_register $test_mgr default_gui");    #Add default GUI user

   # Add some IP addresses to the ports
   initIpAddresses();

   # Add our endpoints
   addCrossConnects();

   my $rl = 0;
   for ( $rl = 0 ; $rl < $start_stop_iterations ; $rl++ ) {
      if ( ( $rl % 2 ) == 0 ) {
         doCmd("set_cx_state $test_mgr all RUNNING");
      }
      else {

         # Do one at a time
         my $q = 0;
         for ( $q = 0 ; $q < @cx_names ; $q++ ) {
            my $cmd = "set_cx_state $test_mgr " . $cx_names[$q] . " RUNNING";
            doCmd($cmd);
         }
      }

      print "Done starting endpoints...sleeping $run_for_time seconds.\n";
      sleep($run_for_time);

      # Now, stop them...

      if ( ( $rl % 2 ) == 0 ) {
         doCmd("set_cx_state $test_mgr all STOPPED");
      }
      else {

         # Do one at a time
         my $q = 0;
         for ( $q = 0 ; $q < @cx_names ; $q++ ) {
            my $cmd = "set_cx_state $test_mgr " . $cx_names[$q] . " STOPPED";
            doCmd($cmd);
         }
      }

      sleep($stop_for_time);

   }    # For some amount of start_stop iterations...
}    # for some amount of loop iterations

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
}    #initToDefaults

sub initPortsToDefault {

   # Set all ports we are messing with to known state.
   my $i = 0;
   for ( $i = 0 ; $i < @lf1_ports ; $i++ ) {
      my $tmp  = $lf1_ports[$i];
      my $tmp2 = $lf2_ports[$i];
      doCmd("set_port $shelf_num $lf1 $tmp 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
      doCmd("set_port $shelf_num $lf2 $tmp2 0.0.0.0 0.0.0.0 0.0.0.0 NA NA NA");
   }
}

sub initIpAddresses {

   # Set all ports we are messing with to known state.
   my $i = 0;
   for ( $i = 0 ; $i < @lf1_ports ; $i++ ) {
      my $tmp  = $lf1_ports[$i];
      my $tmp2 = $lf2_ports[$i];
      my $cmd =
          "set_port $shelf_num $lf1 $tmp "
        . $lf1_port_ips[$i]
        . " 255.255.255.0 "
        . $lf1_port_gws[$i]
        . " NA NA NA";
      doCmd($cmd);
      $cmd =
          "set_port $shelf_num $lf2 $tmp2 "
        . $lf2_port_ips[$i]
        . " 255.255.255.0 "
        . $lf2_port_gws[$i]
        . " NA NA NA";
      doCmd($cmd);
   }
}

sub addCrossConnects {
   my $ep = 0;
   my $cx = 0;
   my $i  = 0;
   for ( $i = 0 ; $i < @cx_types ; $i++ ) {
      my $j = 0;
      for ( $j = 0 ; $j < @lf1_ports ; $j++ ) {
         my $burst = "NO";
         if ( $min_rate != $max_rate ) {
            $burst = "YES";
         }
         my $szrnd = "NO";
         if ( $min_pkt_szs[$i] != $max_pkt_szs[$i] ) {
            $szrnd = "YES";
         }

         my $pattern = "increasing";
         if ( $cx_types[$i] =~ /custom/ ) {
            $pattern = "custom";
         }

         my $ep1 = "endp-${ep}-TX";
         $ep++;
         my $ep2 = "endp-${ep}-RX";
         $ep++;

         @endpoint_names = ( @endpoint_names, $ep1, $ep2 );

         my $cmd =
             "add_endp $ep1 $shelf_num $lf1 "
           . $lf1_ports[$j] . " "
           . @cx_types[$i]
           . " -1 $burst $min_rate $max_rate $szrnd "
           . $min_pkt_szs[$i] . " "
           . $max_pkt_szs[$i]
           . " $pattern NO";
         doCmd($cmd);

         $cmd =
             "add_endp $ep2 $shelf_num $lf2 "
           . $lf2_ports[$j] . " "
           . @cx_types[$i]
           . " -1 $burst $min_rate $max_rate $szrnd "
           . $min_pkt_szs[$i] . " "
           . $max_pkt_szs[$i]
           . " $pattern NO";
         doCmd($cmd);

         # Now, add the cross-connects
         my $cx_name = "cx-${cx}";
         $cmd = "add_cx $cx_name $test_mgr $ep1 $ep2";
         doCmd($cmd);
         doCmd("set_cx_report_timer $test_mgr $cx_name $report_timer");

         $cx++;

         @cx_names = ( @cx_names, $cx_name );

      }    #for all ports
   }    #for all endpoint types
}    #addCrossConnects

sub doCmd {
   my $cmd = shift;

   print ">>> $cmd\n";

   $t->print($cmd);
   my @rslt = $t->waitfor('/ \>\>RSLT:(.*)/');
   print "**************\n @rslt ................\n\n";

   #sleep(1);
}
