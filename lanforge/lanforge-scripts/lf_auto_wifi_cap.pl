#!/usr/bin/perl -w

# This program is used to automatically run LANforge-GUI WiFi Capacity tests.

# Written by Candela Technologies Inc.
#  Udated by:
#
#

use strict;
use warnings;
use Carp;

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
use Cwd;

use constant      NA          => "NA";
use constant      NL          => "\n";
use constant      shelf_num   => 1;

# Default values for ye ole cmd-line args.
our $use_existing_sta = 0;
our $use_existing_cfg = 0;
our $resource         = 1;
our $upstream_resource = -1;
our $quiet            = "yes";
our $radio            = "";  # wiphy0
our $ssid             = "my-ssid";
our $num_sta          = 64;
our $speed_ul         = 0;
our $ul_ps_rate       = 0;
our $speed_dl         = 100000000;
our $dl_ps_rate       = 0;
our $endp_type        = "mix";
our $percent_tcp      = 50;
our $first_ip         = "DHCP";
our $upstream         = "eth1";
our $increment        = 5;
our $duration         = 30;
our $test_name        = "lanforge-wifi-capacity-test";
our $rpt_timer        = 1000;
our $settle_timer     = 10000; # 10 seconds

our $fail_msg         = "";
our $manual_check     = 0;
our $gui_host         = "127.0.0.1";
our $gui_port         = 7777;
our $lfmgr_host       = "127.0.0.1";
our $lfmgr_port       = 4001;
our @test_text        = ();
our $use_pdu_mix      = "false";
our $pdu_percent      = "pps";
our @pdu_mix          = ();
our $use_stations     = "";
our @user_stations    = ();
our $multicon         = -1;

########################################################################
# Nothing to configure below here, most likely.
########################################################################

our $usage = "$0
  [--mgr       {host-name | IP}]
  [--mgr_port  {ip port}]
  [--resource  {number}]
  [--upstream_resource  {number}]
  [--gui_host  {LANforge gui_host (127.0.0.1)}]
  [--gui_port  {LANforge gui_port (7777)}]
  [--radio {name,name2,..}] example:  wiphy0,wiphy1
  [--speed_dl  {speed in bps}]
  [--dl_ps_rate {(0) total download rate, 1 download rate per station}]
  [--speed_ul  {speed in bps}]
  [--ul_ps_rate {(0) total upload rate, 1 upload rate per station}]
  [--ssid      {ssid}]
  [--num_sta   {num-stations-per-radio}]  # For each radio.
  [--use_existing_sta ]  # Assume stations are already properly created and do not re-create.
  [--use_existing_cfg ]  # Use existing station config
  [--upstream  {upstream-port-name (eth1)}]
  [--first_ip  {first-ip-addr | DHCP}]
  [--percent_tcp {percent_tcp for mixed traffic type}]
  [--increment {station-bringup-increment (5)}]
  [--duration  {bringup-step-duration (30)}]
  [--report_timer  {milisecond report timer for created the endpoints (1000)}]
  [--endp_type { udp, tcp, mix }
  [--use_pdu_mix { true | (false) }]
  [--pdu_percent { bps | (pps) }]
  [--pdu_mix   { pdu-size:%, pdu-size:%, ... }]
  [--use_station   { sta1,sta2, ... }]  # Specify which stations to use.
  [--test_name { my-test-name}]
  [--test_text { 'my-test<br>over the air<br>funky-hardware-x<br>OS z'}]
  [--multicon  { -1: auto, 0 none, 1 new process, 2+ new process + multiple streams}
  [--quiet     { yes | no }]

Example:

./lf_auto_wifi_cap.pl --mgr ben-ota-1 --resource 2 --radio wiphy0 --speed_dl 500000000 --ssid Lede-ventana --num_sta 64 --upstream eth1 --first_ip DHCP --percent_tcp 50 --increment 1,5,10,20,30,40,50,64 --duration 15 --report_timer 3000 --endp_type mix --test_name ventana-mix-dl --test_text 'Ventana LEDE, WLE900VX<br>over-the-air to LANforge station system 5 feet away<br>LAN to WiFi traffic path' --multicon 1

";

my $i = 0;
my $help = 0;

GetOptions
(
        'mgr|m=s'       => \$::lfmgr_host,
        'mgr_port=i'    => \$::lfmgr_port,
        'gui_host=s'    => \$::gui_host,
        'gui_port=i'    => \$::gui_port,
        'resource=i'    => \$::resource,
        'upstream_resource=i'    => \$::upstream_resource,
        'radio=s'       => \$::radio,
        'speed_ul=i'    => \$::speed_ul,
        'ul_ps_rate=i'  => \$::ul_ps_rate,
        'speed_dl=i'    => \$::speed_dl,
        'dl_ps_rate=i'  => \$::dl_ps_rate,
        'ssid=s'        => \$::ssid,
        'num_sta=i'     => \$::num_sta,
        'use_existing_sta' => \$::use_existing_sta,
        'use_existing_cfg' => \$::use_existing_cfg,
        'upstream=s'    => \$::upstream,
        'first_ip=s'    => \$::first_ip,
        'percent_tcp=i' => \$::percent_tcp,
        'increment=s'   => \$::increment,
        'duration=i'    => \$::duration,
        'report_timer=i' => \$::rpt_timer,
        'settle_timer=i' => \$::settle_timer,
        'endp_type=s'   => \$::endp_type,
        'test_name=s'   => \$::test_name,
        'multicon=i'    => \$::multicon,
        'test_text=s'   => \$::test_text,
        'use_pdu_mix=s' => \$::use_pdu_mix,
        'pdu_percent=s' => \$::pdu_percent,
        'pdu_mix=s'     => \@::pdu_mix,
        'use_station=s' => \$::use_stations,
        'quiet|q=s'     => \$::quiet,
        'help'          => \$::help,
) || die("$::usage");

if ($::help) {
  print $::usage;
  exit(0);
}

if ($use_stations ne "") {
  @user_stations = split(",", $use_stations);
}

if ($upstream_resource == -1) {
  $upstream_resource = $resource;
}

our $mgr_telnet = new Net::Telnet(Prompt => '/default\@btbits\>\>/',
          Timeout => 20);
$::mgr_telnet->open(Host    => $lfmgr_host,
         Port    => $lfmgr_port,
         Timeout => 10);
$::mgr_telnet->waitfor("/btbits\>\>/");

# Configure our utils.
our $utils = new LANforge::Utils();
$utils->telnet($::mgr_telnet);         # Set our telnet object.
if ($utils->isQuiet()) {
  if (defined $ENV{'LOG_CLI'} && $ENV{'LOG_CLI'} ne "") {
    $utils->cli_send_silent(0);
  }
  else {
    $utils->cli_send_silent(1); # Do not show input to telnet
  }
  $utils->cli_rcv_silent(1);  # Repress output from telnet
}
else {
  $utils->cli_send_silent(0); # Show input to telnet
  $utils->cli_rcv_silent(0);  # Show output from telnet
}
$utils->log_cli("# $0 ".`date "+%Y-%m-%d %H:%M:%S"`);

my @radios = split(/,/, $::radio);
my $starting_sta = 500;
my $first_sta = $starting_sta;

if (@radios == 0) {
  print ("No radios specified, doing nothing.\n");
  exit(1);
}

if (!$::use_existing_sta) {
  # Clean ports on these radios.
  for ($i = 0; $i<@radios; $i++) {
    my $r = $radios[$i];
    print "Deleting virtual devices on resource $::resource radio: $r\n";
    system("./lf_associate_ap.pl  --mgr $::lfmgr_host --mgr_port $::lfmgr_port --resource $::resource --action del_all_phy --port_del $r");
  }
}

if (!$::use_existing_cfg) {
  # Create/Set stations on these radios.
  for ($i = 0; $i<@radios; $i++) {
    my $r = $radios[$i];

    print "Creating/Setting $::num_sta virtual stations on resource $::resource radio: $r\n";
    system("./lf_associate_ap.pl --mgr $::lfmgr_host --mgr_port $::lfmgr_port --resource $::resource "
	   ." --action add --radio $r --ssid $::ssid "
	   ." --first_sta sta$first_sta --first_ip $::first_ip "
	   ." --num_stations $::num_sta --admin_down_on_add");
    $first_sta += $::num_sta;
  }
}

my $cwd = cwd();
my $wifi_cap_fname = "wifi_auto_cap_" . $$ . ".txt";

# Create temporary wifi capacity config file.
open(CAP, ">$wifi_cap_fname") or die ("Can't open $wifi_cap_fname for writing.\n");

print CAP "__CFG VERSION 1\n";
print CAP "__CFG SEL_PORT 1 $::upstream_resource $::upstream\n";

our @sta_list = ();
if (@user_stations) {
  # Use all existing stations on the specified radio
  for ($i = 0; $i<@user_stations; $i++) {
    my $sta_name = $user_stations[$i];
    print CAP "__CFG SEL_PORT 1 $::resource $sta_name\n";
    push(@sta_list, "$sta_name");
  }
}
else {
  for ($i = $starting_sta; $i<$first_sta; $i++) {
    print CAP "__CFG SEL_PORT 1 $::resource sta$i\n";
    push(@sta_list, "sta$i");
  }
}

print CAP "__CFG STA_INCREMENT $::increment\n";
print CAP "__CFG DURATION " . ($::duration * 1000) . "\n";
print CAP "__CFG RPT_TIMER " . ($::rpt_timer) . "\n";
print CAP "__CFG BEFORE_CLEAR " . ($::settle_timer) . "\n";

my $proto = 0;
if ($endp_type eq "tcp") {
  $proto = 1;
}
# 2 is layer-4, this script does not support that currently.
elsif ($endp_type eq "mix") {
  $proto = 3;
}
print CAP "__CFG PROTOCOL $proto\n";
print CAP "__CFG DL_RATE_SEL $::dl_ps_rate\n";
print CAP "__CFG DL_RATE $::speed_dl\n";
print CAP "__CFG UL_RATE_SEL $::ul_ps_rate\n";
print CAP "__CFG UL_RATE $::speed_ul\n";
print CAP "__CFG PRCNT_TCP " . ($::percent_tcp * 10000) . "\n";
print CAP "__CFG MULTI_CONN $::multicon\n";
print CAP "__CFG USE_MIX_PDU $::use_pdu_mix\n";

my $pps = "false";
my $bps = "false";
if ($pdu_percent eq "pps") {
  $pps = "true";
}
elsif ($pdu_percent eq "bps") {
  $bps = "true";
}
print CAP "__CFG PDU_PRCNT_PPS $pps\n";
print CAP "__CFG PDU_PRCNT_BPS $bps\n";

#my @pdu_mix_ln = split(/,/, $::pdu_mix);
for ($i = 0; $i < @::pdu_mix; $i++) {
  print CAP "__CFG PDU_MIX_LN " . $::pdu_mix[$i] . "\n";
}

my @test_texts = split(/<br>/, $::test_text);
for ($i = 0; $i < @test_texts; $i++) {
  print CAP "__CFG NOTES_TEXT_LN " . $test_texts[$i] . "\n";
}

# Things not specified will be left at defaults.

close(CAP);
my $accounted_for = 0;
while ($accounted_for < $::num_sta) {
   my @show_lines = split("\n", $::utils->doAsyncCmd("nc_show_ports 1 $::resource ALL"));
   sleep 2;
   $accounted_for = 0;
   for my $sta_name (@sta_list) {
      my @sta_matches = grep { / $sta_name /} @show_lines;
      if (@sta_matches > 0) {
         #print "  found: ".join("\n", @sta_matches)."\n";
         $accounted_for++;
      }
   } # ~for each station
   print " $accounted_for/$::num_sta up\n";
}
# sleep 2s extra because one station might not be quite done setting up whereas
# 10 station will overall less time per station
sleep 2;

#  Send command to GUI to start this test.
# Something like:  wifi_cap run "ventana-mix-dl" "/tmp/ventana-dl-0003"
our $gui_telnet = new Net::Telnet(Prompt => '/#/',
                                  Timeout => 60);
$::gui_telnet->open(Host    => $::gui_host,
                    Port    => $::gui_port,
                    Timeout => 10);
$::gui_telnet->waitfor("/#/");

my $output_dname = "$::test_name" . "_" . time();
my $output_fname = "$cwd/$output_dname";
my $cmd = "wifi_cap run \"$cwd/$wifi_cap_fname\" \"$output_fname\"\n";
print "Sending GUI command to start the capacity test -:$cmd:-\n";
my @rslt = $::gui_telnet->cmd($cmd);
$::gui_telnet->close();

print "GUI result: " . join(@rslt, "\n");
print "Waiting for test to complete...\n";
# Wait until test is done.
while (1) {
  if (-f "$output_fname/index.html") {
    print "Found $output_fname/index.html, wait one more minute to be sure images are written.\n";
    last;
  }
  sleep(10);
}

# Could still take a bit to complete writing out the images...
sleep(60);

print "Finished, see report at: $output_fname/index.html\n";

system("tar -cvzf $output_dname.tar.gz $output_dname");

# Notes on possible LEDE/OpenWRT DUT cleanup
# rm /etc/dhcp.leases and reboot to clean leases.
