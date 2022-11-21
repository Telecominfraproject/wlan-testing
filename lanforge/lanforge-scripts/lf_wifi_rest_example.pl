#!/usr/bin/perl

# This program is used to stress test the LANforge system, and may be used as
# an example for others who wish to automate LANforge tests.

# If Net::Telnet is not found, try:  yum install "perl(Net::Telnet)"

# If the LANforge libraries are not found, make sure you are running
# from the /home/lanforge directory (or where-ever you installed LANforge)

# Contact:  support@candelatech.com if you have any questions or suggestions
#   for improvement.

# Written by Candela Technologies Inc.
#  Updated by: greearb@candelatech.com
#
#
#  This script creates some stations, creates some connections on them, runs them, gathers
#  some upload/download results, and then stops the connections.  It is a good example of
#  how to call other LANforge scripts to more easily get work done.
#
#
#  You may need to install perl-JSON:  dnf install perl-JSON
#


use strict;
use warnings;
#use Carp;
# Un-buffer output
$| = 1;

use LANforge::Endpoint;
use LANforge::Port;
use LANforge::Utils;
use Net::Telnet ();
use Getopt::Long;
use JSON;
use Data::Dumper;
use LANforge::GuiJson qw(GuiResponseToHash GetHeaderMap GetRecordsMatching GetFields);

#use constant   NL    => "\n";
my $lfmgr_port       = 4001;
my $shelf_num        = 1;
# Specify 'card' numbers for this configuration.

my $amt_resets_sofar = 0;
my $report_timer = 1000;  # 1 second report timer, hard-coded for now.

# Default values for ye ole cmd-line args.

my $lfmgr_host       = "localhost";
my $card             = 1;
my $upstream         = "eth1";
my $port_name        = "";
my $station_count    = "";
my $radio            = "wiphy0";
our $quiet           = 0;
my $amt_resets       = 1;
my $min_sleep        = 30;
my $max_sleep        = 30;
my $fail_msg         = "";
my $manual_check     = 0;
my $show_port        = undef;
my @port_stats       = ();
my $cmd_log_name     = ""; #= "lf_portmod.txt";
my $set_speed        = "NA";
my $wifi_mode        = "NA";
my $security         = "open";
my $passwd           = "NA";
my $ssid             = "NA";
my $ap               = "NA";
my $eap_identity     = "NA";
my $eap_passwd       = "NA";
my $cx_type          = "udp";
my $speedA           = "64000";
my $speedB           = "64000";
my $log_file         = "";
my $NOT_FOUND        = "-not found-";
my $load             = "";

########################################################################
# Nothing to configure below here, most likely.
########################################################################


my $usage = "$0  --port_name {name | number}
[--manager        { network address of LANforge manager} ]
[--amt_resets     { number (0 means forever) } ]
[--upstream       { port-name } ]
[--radio          { radio-name } ]
[--station_count  { number } ]
[--cx_type        { lf_tcp, lf_udp, lf_tcp6, lf_udp6 } ]
[--speedA         { transmit speed for endpoint A }
[--speedB         { transmit speed for endpoint B }
[--min_sleep      { minimum number (seconds) to run the connections } ]
[--max_sleep      { maximum number (seconds) to run the connections} ]
[--load|-L        { db-name } ]
[--card           { card-id } ]
[--quiet          { level } ]
[--set_ifstate    {up | down} ]
[--show_port      [key,key,key]]
   # show all port stats or just those matching /key:value/
[--set_speed      {wifi port speed, see GUI port-modify drop-down for possible values. Common
                   examples: 'OS Defaults', '6 Mbps a/g', '1 Stream  /n', '2 Streams /n', MCS-0 (x1 15 M), MCS-10 (x2 90 M),
                             'v-MCS-0 (x1 32.5 M)', 'v-1 Stream  /AC', 'v-2 Streams /AC', ... }
[--wifi_mode      {wifi mode: 0: AUTO, 1: 802.11a, 2: b, 3: g, 4: abg, 5: abgn,
                              6: bgn 7: bg, 8: abgnAC, 9 anAC, 10 an}
                  # wifi-mode option is applied when --set_speed is used.
[--security       {open|wep|wpa|wpa2}
[--passwd         {WiFi WPA/WPA2/ password}
[--ssid           {WiFi SSID}
[--ap             {BSSID of AP, or 'DEFAULT' for any.}
[--eap_identity   {value|[BLANK]}]
[--eap_passwd     {value|[BLANK]}]
[--log_file|--log {value}] # disabled by default
[--help|-h        # show help ]

Examples:
./lf_wifi_rest_example.pl --manager localhost --card 1 --port_name sta010 --station_count 5 --ssid Lede-apu2-AC \
     --radio wiphy0 --quiet 1 --upstream eth5 --speedB 15000000
";

my $i = 0;
my $log_cli = 'unset';
my $show_help =0;
GetOptions
(
 'help|h'            => \$show_help,
 'ap=s'              => \$ap,
 'port_name|e=s'     => \$port_name,
 'upstream=s'        => \$upstream,
 'radio=s'           => \$radio,
 'station_count=s'   => \$station_count,
 'cx_type=s'         => \$cx_type,
 'manager|m=s'       => \$lfmgr_host,
 'load|L=s'          => \$load,
 'quiet|q=s'         => \$::quiet,
 'card|C=i'          => \$card,
 'amt_resets=i'      => \$amt_resets,
 'min_sleep=i'       => \$min_sleep,
 'max_sleep=i'       => \$max_sleep,
 'passwd=s'          => \$passwd,
 'set_speed=s'       => \$set_speed,
 'speedA=s'          => \$speedA,
 'speedB=s'          => \$speedB,
 'ssid=s'            => \$ssid,
 'show_port:s'       => \$show_port,
 'port_stats=s{1,}'  => \@port_stats,
 'eap_identity|i=s'  => \$eap_identity,
 'eap_passwd|p=s'    => \$eap_passwd,
 'log_file|log=s'      => \$log_file,
 'log_cli=s{0,1}'    => \$log_cli,
 'wifi_mode=i'       => \$wifi_mode,
 ) || (print($usage) && exit(1));

if ($show_help) {
   print $usage;
   exit 0;
}

 if ($::quiet eq "0") {
   $::quiet = "no";
 }
 elsif ($::quiet eq "1") {
   $::quiet = "yes";
 }

# Configure logging...
if (defined $log_cli) {
  if ($log_cli ne "unset") {
    # here is how we reset the variable if it was used as a flag
    if ($log_cli eq "") {
      $ENV{'LOG_CLI'} = 1;
    }
    else {
      $ENV{'LOG_CLI'} = $log_cli;
    }
  }
}

# Open connection to the LANforge server.  We use this for direct
# calls to the LANforge CLI.
my $t = new Net::Telnet(Prompt => '/default\@btbits\>\>/',
         Timeout => 20);

$t->open(Host => $lfmgr_host,
      Port    => $lfmgr_port,
      Timeout => 10);

$t->waitfor("/btbits\>\>/");

my $dt = "";

# Configure our utils.
our $utils = new LANforge::Utils();
$::utils->telnet($t);
if ($::utils->isQuiet()) {
  if (defined $ENV{'LOG_CLI'} && $ENV{'LOG_CLI'} ne "") {
    $::utils->cli_send_silent(0);
  }
  else {
    $::utils->cli_send_silent(1); # Do not show input to telnet
  }
  $::utils->cli_rcv_silent(1);  # Repress output from telnet
}
else {
  $::utils->cli_send_silent(0); # Show input to telnet
  $::utils->cli_rcv_silent(0);  # Show output from telnet
}
$::utils->log_cli("# $0 ".`date "+%Y-%m-%d %H:%M:%S"`);
if (defined $log_file && ($log_file ne "")) {
   open(CMD_LOG, ">$log_file") or die("Can't open $log_file for writing...\n");
   $cmd_log_name = $log_file;
   if (!$::utils->isQuiet()) {
      print "History of all commands can be found in $log_file\n";
   }
}

if (length($port_name) == 0) {
   print "ERROR:  Must specify port name.\n";
   die("$usage");
}

#  Create a file in which we can store data for generating graphs and such.
my $data_fname = "_graph_data.csv";
open(PLOT_DATA, ">$data_fname");


# Load an initial DB if requested.
if ($load ne "") {
   my $cli_cmd = "load $load overwrite";
   $utils->doAsyncCmd($cli_cmd);
   my @rslt = $t->waitfor("/LOAD-DB:  Load attempt has been completed./");
   if (!$utils->isQuiet()) {
      print @rslt;
      print "\n";
   }
}

# lf_associate names ports thus, and we need to access these ports,
# so build the names here.  This is one place where 'internal' changes
# to lf_associate could cause issues.
my $offset = 100;
if ($port_name =~ /^.*?(\d+)\s*$/) {
  $offset = $1;
}
my @stations = ();
my @cxs = ();
my @epa = ();
my @epb = ();

for ($i = 0; $i < $station_count; $i++) {
  my $suffix = 0 + $i + $offset;
  $stations[$i] = sprintf("sta%03d", $suffix);
  $cxs[$i] = sprintf("cx-%03d", $suffix);
  $epa[$i] = sprintf("ep-A%03d", $suffix);
  $epb[$i] = sprintf("ep-B%03d", $suffix);
}

#  Create some stations using the lf_associate.pl script.
my $cmd = "./lf_associate_ap.pl --mgr $lfmgr_host --mgr_port $lfmgr_port --resource $card " .
  "--action add --radio $radio --ssid $ssid --first_sta $port_name --first_ip DHCP --num_stations " .
  " $station_count --passphrase \"$passwd\" --security $security --wifi_mode $wifi_mode --log_cli";
my $rslt = run_cmd($cmd);

if ($set_speed ne "NA") {
  # lf-associate cannot set the speed currently, so use lf_portmod.pl
  for ($i = 0; $i<@stations; $i++) {
    $cmd = "./lf_portmod.pl --manager $lfmgr_host --card $card --port_name " . $stations[$i] . " --set_speed \"$set_speed\"";
    $rslt = run_cmd($cmd);
  }
}

# Make sure stations are admin up, in case they were previously created and admin-down.
for ($i = 0; $i<@stations; $i++) {
  $cmd = "./lf_portmod.pl --manager $lfmgr_host --card $card --port_name " . $stations[$i] . " --set_ifstate up";
  $rslt = run_cmd($cmd);
}

# Create some Layer-3 connections for data generation.
for ($i = 0; $i<@stations; $i++) {
  # Remove any old ones first
  # A-side connection on station.
  $cmd = "rm_cx all " . $cxs[$i];
  $utils->doCmd($cmd);
  $cmd = "rm_endp " . $epa[$i];
  $utils->doCmd($cmd);
  $cmd = "rm_endp " . $epb[$i];
  $utils->doCmd($cmd);

  # And create some new ones...
  # A-side connection on station.
  $cmd = "./lf_firemod.pl --mgr $lfmgr_host --mgr_port $lfmgr_port --resource $card --action create_endp --endp_name "
    . $epa[$i] . " --speed $speedA --endp_type $cx_type --report_timer $report_timer --port_name " . $stations[$i];
  $rslt = run_cmd($cmd);

  # B-side connection on upstream port
  $cmd = "./lf_firemod.pl --mgr $lfmgr_host --mgr_port $lfmgr_port --resource $card --action create_endp --endp_name "
    . $epb[$i] . " --speed $speedB --endp_type $cx_type --report_timer $report_timer --port_name $upstream";
  $rslt = run_cmd($cmd);

  # Create a connection.
  $cmd = "./lf_firemod.pl --mgr $lfmgr_host --mgr_port $lfmgr_port --resource $card --report_timer $report_timer --action create_cx --cx_name "
    . $cxs[$i] . " --cx_endps " . $epa[$i] . "," . $epb[$i];
  $rslt = run_cmd($cmd);
}

# Wait for ports to associate.
my $max_wait = 30;
for ($i = 0; ; $i++) {
  my $q;
  my $not_assoc = 0;
  my $no_ip = 0;
  for ($q = 0; $q < @stations; $q++) {
    $cmd = "./lf_portmod.pl  --manager $lfmgr_host --card $card -q yes --port_name " . $stations[$q] . " --show_port AP,IP";
    $rslt = run_cmd($cmd);
    if ($rslt =~ /Not-Associated/) {
      $not_assoc++;
    }
    if ($rslt =~ /IP:\s+0.0.0.0/) {
      $no_ip++;
    }
  }
  if ($not_assoc || $no_ip) {
    if ($i > $max_wait) {
      print("ERROR:  Could not connect or get IPs for all stations, continuing...\n");
      last;
    }
    sleep(1);
  }
  else {
    print("All ports are associated and have IP...\n");
    last;
  }
}


#  Start with slow speed previously set so ARP can complete easily....
#  Start our cross-connects by directly calling into LANforge CLI.
for ($i = 0; $i<@cxs; $i++) {
  my $cmd = "set_cx_state all " . $cxs[$i] . " running";
  $utils->doAsyncCmd($cmd);
}

# LANforge 5.3.7 GUI has 'cli' cmd to run arbitrary commands.  So, ask it
# to refresh the endpoints and cx now that they are running.  This will only
# work on a unix-like system, but one could use a real tcp connection with a bit
# more work.  Assumes GUI is running with option: -cli-socket 3990 on the local machine.
$cmd = "echo -e cli show_endp\\\\ncli show_port\\\\ncli show_cx\\\\nexit | nc localhost 3990";
#print("Running cmd: $cmd\n");
$rslt = `$cmd`;
#print $rslt;


print("Sleeping 5 seconds to let connections initialize...\n");
sleep(5);

# Clear port counters, this will make their running averages more accurate,
# and any byte/pkt totals gathered at the end would also be more useful.
for ($i = 0; $i<@stations; $i++) {
  my $cmd = "clear_port_counters $shelf_num $card " . $stations[$i];
  $utils->doCmd($cmd);
}

$cmd = "clear_port_counters $shelf_num $card $upstream";
$utils->doCmd($cmd);

# Set connections to desired speed and clear counters.
for ($i = 0; $i<@cxs; $i++) {
  my $cmd = "add_endp " . $epa[$i] . " NA NA NA NA NA NA NA $speedA";
  $utils->doAsyncCmd($cmd);
  $cmd = "add_endp " . $epb[$i] . " NA NA NA NA NA NA NA $speedB";
  $utils->doAsyncCmd($cmd);

  $cmd = "clear_cx " . $cxs[$i];
  $utils->doAsyncCmd($cmd);
}

my $start = time();

# Calculate how long to run the connections.
my $run_time = $min_sleep;
if ($max_sleep > $min_sleep) {
  $run_time += int(rand($max_sleep - $min_sleep));
}

my $total_dl;
my $total_ul;
do {
  # Gather some stats.  Note that connections do not start exactly
  # at the same time, nor exactly when we ask them to, so we query the
  # connection for the 'running-for' time and calculate stats based on that
  # for best precision.  Once a connection has been running for at least 60 seconds,
  # then we can just use the pre-calculated 60-second running average.
  #
  # For LANforge 5.3.6 and earlier, the 'RunningFor' output is in whole seconds only,
  # so there will be some rounding errors when we have only been running for a few seconds.
  # LANforge 5.3.7 and above will provide a fractional-second output to make the stats
  # more precise.
  my $total_dl = 0;
  my $total_ul = 0;
  my $total_dl_bps = 0;
  my $total_ul_bps = 0;

  for ($i = 0; $i<@cxs; $i++) {

    # Grab stats for endpoint A.  This could be made into a method call to
    # decrease duplicated code.
    $rslt = $utils->doAsyncCmd("nc_show_endp " . $epa[$i] . "\n");
    if ($rslt =~ /Rx Bytes:\s+Total: (\d+)\s+Time: 60s\s+Cur: (\d+)\s+(\d+)\/s/) {
      my $bytes = $1;
      my $cur = $2;
      my $per_min = $3;
      my $rf = -1;
      my $avg = 0;
      if (($rslt =~ /RunningFor:\s+(\d+)s/) ||
	  ($rslt =~ /RunningFor:\s+(\d+.\d+)s/)) {
	$rf = $1;
      }
      if ($rf < 60) {
	if ($rf > 0) {
	  $avg = (($cur * 8) / $rf);
	}
	else {
	  $avg = 0;
	}
      }
      else {
	$avg = $per_min * 8;
      }
      #print("endp: " . $epa[$i] . " rx-bytes: $bytes  running-for: $rf avg-bps: $avg\n");
      $total_dl += ($bytes * 8);
      $total_dl_bps += $avg;
    }
    else {
      print("ERROR:  Cannot parse result: $rslt\n");
    }

    # Grab stats for endpoint B
    $rslt = $utils->doAsyncCmd("nc_show_endp " . $epb[$i] . "\n");
    if ($rslt =~ /Rx Bytes:\s+Total: (\d+)\s+Time: 60s\s+Cur: (\d+)\s+(\d+)\/s/) {
      my $bytes = $1;
      my $cur = $2;
      my $per_min = $3;
      my $rf = -1;
      my $avg = 0;
      if (($rslt =~ /RunningFor:\s+(\d+)s/) ||
	  ($rslt =~ /RunningFor:\s+(\d+.\d+)s/)) {
	$rf = $1;
      }
      if ($rf < 60) {
	if ($rf > 0) {
	  $avg = (($cur * 8) / $rf);
	}
	else {
	  $avg = 0;
	}
      }
      else {
	$avg = $per_min * 8;
      }

      #print(" endp: " . $epb[$i] . " rx-bytes: $bytes  running-for: $rf avg-bps: $avg\n");
      $total_ul += ($bytes * 8);
      $total_ul_bps += $avg;
    }
    else {
      print("ERROR:  Cannot parse result: $rslt\n");
    }
  }

  # Print and store bps data for this loop iteration.
  my $now = time();
  print("$now:  60-sec running average:  total-download-bps: $total_dl_bps   total-upload-bps: $total_ul_bps\n");
  my $rel_t = $now - $start;
  if ($rel_t) {  # Skip 0 time, no data available.
    # Convert to mbps
    $total_dl_bps /= 1000000;
    $total_ul_bps /= 1000000;
    my $tot_ul_dl = $total_dl_bps + $total_ul_bps;
    print PLOT_DATA "$rel_t\t$total_dl_bps\t$total_ul_bps\t$tot_ul_dl\n";
  }

  sleep(1);
} while (time() < ($start + $run_time));


#  Stop our cross-connects by directly calling into LANforge CLI.
for ($i = 0; $i<@cxs; $i++) {
  my $cmd = "set_cx_state all " . $cxs[$i] . " stopped";
  $utils->doCmd($cmd);
}

# Refresh GUI stats before we query JSON.
$cmd = "echo -e cli show_port\\\\ncli show_cx\\\\nexit | nc localhost 3990";
#print("Running cmd: $cmd\n");
$rslt = `$cmd`;

# Wait 2 seconds for reports to come back to the GUI.
sleep(2);

# Gather some stats using JSON.  This assumes the GUI is running on the local machine on port 8080
# [lanforge@lf0313-6477 LANforgeGUI_5.3.7]$ pwd
# /home/lanforge/LANforgeGUI_5.3.7
# [lanforge@lf0313-6477 LANforgeGUI_5.3.7]$ ./lfclient.bash -httpd 8080
#

# Get a JSON dump of all rows and columns on the LANforge GUI Ports Tab.
my $gjson = new LANforge::GuiJson();
$gjson->Request("http://localhost:8080/PortTab");

# Grab data for these fields for all of our ports in use in this test.
my @field_names = ("bps TX", "bps RX", "TX-Rate", "RX-Rate", "AP", "Channel", "CX Time.*");
my @port_names = (@stations, $upstream);
my $ra_fields = $gjson->GetFields('Device', \@port_names, \@field_names);

# And print out the JSON data on the console.  This is just an example, you may
# instead wish to grab different data and graph it and/or poke it into some long-term
# storage for future comparisons.
print "Fields (".join(", ", @field_names).") from records matching Device (".join(", ", @port_names)."):\n";
print Dumper($ra_fields);


# Create some gnuplot graphs.  Probably there is a more clever way to do this by
# passing arguments to gnuplot, but I am faster at perl than understanding gnuplot
# at this point...

my $gp_base = "# gnuplot script file for plotting bandwidth over time
#!/usr/bin/gnuplot
reset
set terminal png

set xdata time
set timefmt \"\%s\"
set format x \"\%M:\%S\"

set xlabel \"Date\"
set ylabel \"__YLABEL__\"

set title \"__TITLE__\"
set key below
set grid
plot \"$data_fname\" using __USING__ title \"__TITLE__\" with lines
";

# Do text substitution of the gnuplot script for each graph.
my $script_fname = "_gnuplot_script.txt";
open(GP, ">$script_fname") || die("Can't open $script_fname for writing...\n");
my $gpd = $gp_base;
$gpd =~ s/__YLABEL__/Total Mbps Download/g;
$gpd =~ s/__TITLE__/Total Mbps Download over Time/g;
$gpd =~ s/__USING__/1\:2/g;

print GP $gpd;
close(GP);
system("gnuplot \"$script_fname\" > download_bps.png");

open(GP, ">$script_fname") || die("Can't open $script_fname for writing...\n");
$gpd = $gp_base;
$gpd =~ s/__YLABEL__/Total Mbps Upload/g;
$gpd =~ s/__TITLE__/Total Mbps Upload over Time/g;
$gpd =~ s/__USING__/1\:3/g;

print GP $gpd;
close(GP);
system("gnuplot \"$script_fname\" > upload_bps.png");

open(GP, ">$script_fname") || die("Can't open $script_fname for writing...\n");
$gpd = $gp_base;
$gpd =~ s/__YLABEL__/Total Mbps Upload+Download/g;
$gpd =~ s/__TITLE__/Total Mbps Upload+Download over Time/g;
$gpd =~ s/__USING__/1\:4/g;

print GP $gpd;
close(GP);
system("gnuplot \"$script_fname\" > ul_dl_bps.png");

print("See gnuplot generated files: ul_dl_bps.png, download_bps.png, upload_bps.png\n");

close(CMD_LOG);
exit(0);


sub run_cmd {
  my $cmd = shift;
  if (!$utils->isQuiet()) {
    print $cmd;
    print "\n";
  }
  my $rslt = `$cmd`;
  if (!$utils->isQuiet()) {
    print $rslt;
    print "\n";
  }
  return $rslt;
}
