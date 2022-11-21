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

package main;
use strict;
use warnings;
use diagnostics;
use Data::Dumper;
use Carp;
$SIG{ __DIE__  } = sub { Carp::confess( @_ ) };
$SIG{ __WARN__  } = sub { Carp::confess( @_ ) };

# Un-buffer output
$| = 1;

use Cwd qw(getcwd);
my $cwd = getcwd();

# use lib prepends to @INC, so put lower priority first
# This is before run-time, so cannot condition this with normal 'if' logic.
use lib '/home/lanforge/scripts';
use lib "../";
use lib "./";

use LANforge::Endpoint;
use LANforge::Port;
use LANforge::Utils;
use Net::Telnet ();
use Getopt::Long;

my $lfmgr_host       = "localhost";
my $lfmgr_port       = 4001;
my $shelf_num        = 1;
# Specify 'card' numbers for this configuration.
my $card             = 1;

# Default values for ye ole cmd-line args.
my $list_port_names;
my $list_ports;
my $filter_ports;
my $port_name        = "";
my $cmd              = "";
our $quiet           = 1;
my $load             = "";
my $amt_resets       = 1;
my $max_port_name    = 0;
my $min_sleep        = 60;
my $max_sleep        = 120;
my $if_state         = "unset";
my $fail_msg         = "";
my $manual_check     = 0;
my $amt_resets_sofar = 0;
my $show_port        = "NA";
my @port_stats       = ();
my $cmd_log_name     = ""; #= "lf_portmod.txt";
my $set_speed        = "NA";
my $set_channel      = "NA";
my $set_nss          = "NA";
my $wifi_mode        = "NA";
my $passwd           = "NA";
my $ssid             = "NA";
my $ap               = "NA";
my $eap_identity     = "NA";
my $eap_passwd       = "NA";
my $cli_cmd          = "";
my $log_file         = "";
my $NOT_FOUND        = "-not found-";
my $stats_from_file  = "";
my $ip = "NA";  # DHCP or IP address
my $netmask = "NA"; # Netmask, only changed when 'IP' is set.
my $gw = "NA"; # Gateway, only changed when 'IP' is set.


########################################################################
# Nothing to configure below here, most likely.
########################################################################

my $usage = << "EOF"
   $0  --port_name {name | number}
--cmd                { reset | delete }
[--manager|--mgr|-m  { network address of LANforge manager} ]
[--manager_port|mgr_port|lf_port|mp { manager port number } ]
[--cli_cmd           { lf-cli-command text } ]
[--amt_resets        { number (0 means forever) } ]
[--max_port_name     { number } ]
[--min_sleep         { number (seconds) } ]
[--max_sleep         { number (seconds) } ]
[--load              { db-name } ]
[--card|--resource|-r { resource-id } ]
[--quiet             { 0|no|1|yes } ]
[--set_ifstate       { up|down } ]
[--list_port_names   # prints port names for resource  ]
[--list_ports        # shows all ports and port details for resource]
[--filter_ports      { keyword } # prints port name and matching value for all ports for resource ]
[--show_port [key,key,key] ]
   # show all port stats or just those matching /key:value/
[--stats_from_file [file-name]
   # Read 'show-port' ouput from a file instead of direct query from LANforge.
   # This can save a lot of time if we already have the show-port output available.
[--set_speed      { wifi port speed, see GUI port-modify drop-down for possible values. Common
                   examples: 'OS Defaults', '6 Mbps a/g', '1 Stream  /n', '2 Streams /n', MCS-0 (x1 15 M), MCS-10 (x2 90 M),
                             'v-MCS-0 (x1 32.5 M)', 'v-1 Stream  /AC', 'v-2 Streams /AC', ... }
[--wifi_mode      { wifi mode: 0: AUTO, 1: 802.11a, 2: b, 3: g, 4: abg, 5: abgn,
                              6: bgn 7: bg, 8: abgnAC, 9 anAC, 10 an}
                  # wifi-mode option is applied when --set_speed is used.
[--set_channel    { for radios, wifi channel (36, 100, etc) }
[--set_nss        { for radios, set spatial streams (1, 2, 3, 4) }
[--passwd         { WiFi WPA/WPA2/ password}
[--ssid           { WiFi SSID}
[--ap             { BSSID of AP, or 'DEFAULT' for any.}
[--eap_identity   { value | [BLANK]}]
[--eap_passwd     { value | [BLANK]}]
[--log_file       { value }] # disabled by default
[--ip             { DHCP | IPv4 Address }]
[--netmask        { network mask, only modified if IP is specified as well.]
[--gw             { network gateway, only modified if IP is specified as well.]
[--help|-h        ] # show help

Examples:
./lf_portmod.pl --manager 192.168.1.101 --resource 1 --list_ports
./lf_portmod.pl --mgr 192.168.1.101 --card 1 --port_name eth2 --show_port
./lf_portmod.pl -m 192.168.1.101 -r 1 --port_name sta1 --show_port AP,ESSID,bps_rx,bps_tx
./lf_portmod.pl -m 192.168.1.101 --card 1 --port_name sta1 --stats_from_file /tmp/ports.txt --show_port AP,ESSID,bps_rx,bps_tx
./lf_portmod.pl -m 192.168.1.101 --cli_cmd "scan 1 1 sta0"
./lf_portmod.pl - 192.168.1.101 --card 1 --port_name eth2 --cmd reset
./lf_portmod.pl -m 192.168.1.101 --card 1 --port_name eth2 --set_ifstate down
./lf_portmod.pl -m 192.168.1.101 --card 1 --port_name eth2 --ip DHCP
./lf_portmod.pl -m 192.168.1.101 --card 1 --port_name eth2 --ip 10.1.1.1 --netmask 255.255.0.0 --gw 10.1.1.254
./lf_portmod.pl -m 192.168.1.101 --card 1 --port_name sta0 --wifi_mode 2 --set_speed "1 Mbps /b" \\
                --ssid fast-ap --passwd "secret passwd" --ap DEFAULT
./lf_portmod.pl -m 192.168.1.101 --card 1 --port_name wiphy0 --set_channel "36" --set_nss 2
./lf_portmod.pl --load my_db
./lf_portmod.pl -m 192.168.100.138 --cmd reset --port_name 2 --amt_resets 5 --max_port_name 8 --card 1 --min_sleep 10 --max_sleep 20
./lf_portmod.pl -m 192.168.1.101 --card 1 --port_name sta11 --cmd set_wifi_extra --eap_identity 'adams' --eap_passwd 'family'

# Set wlan0 to /a/b/g mode, 1Mbps encoding rate
./lf_portmod.pl --manager localhost --card 1 --port_name wlan0 --wifi_mode 4 --set_speed "1 Mbps /b"

# Set wlan0 to /a/b/g mode, default encoding rates
./lf_portmod.pl --manager localhost --card 1 --port_name wlan0 --wifi_mode 4 --set_speed "DEFAULT"

# Set wlan0 to /a/b/g/n mode, default encoding rates for 1 antenna stations (1x1)
./lf_portmod.pl --manager localhost --card 1 --port_name wlan0 --wifi_mode 5 --set_speed "1 Stream  /n"

# Set wlan0 to /a/b/g/n mode, default encoding rates for 2 antenna stations (2x2)
./lf_portmod.pl --manager localhost --card 1 --port_name wlan0 --wifi_mode 5 --set_speed "2 Streams /n"

# Set wlan0 to /a/b/g/n mode, default encoding rates for 3 antenna stations (3x3)
./lf_portmod.pl --manager localhost --card 1 --port_name wlan0 --wifi_mode 5 --set_speed "DEFAULT"

# Set wlan0 to /a/b/g/n/AC mode, default encoding rates for 1 antenna stations (1x1)
./lf_portmod.pl --manager localhost --card 1 --port_name wlan0 --wifi_mode 8 --set_speed "v-1 Stream  /AC"

# Set wlan0 to /a/b/g/n/AC mode, default encoding rates for 2 antenna stations (2x2)
./lf_portmod.pl --manager localhost --card 1 --port_name wlan0 --wifi_mode 8 --set_speed "v-2 Streams /AC"

# Set wlan0 to /a/b/g/n/AC mode, default encoding rates for 3 antenna stations (3x3)
./lf_portmod.pl --manager localhost --card 1 --port_name wlan0 --wifi_mode 8 --set_speed "DEFAULT"
EOF
;

my $i = 0;
my $log_cli = 'unset';
my $show_help = 0;

if (@ARGV < 2) {
   print $usage;
   exit 0;
}
GetOptions
(
 'help|h'            => \$show_help,
 'ap=s'              => \$ap,
 'port_name|e=s'     => \$port_name,
 'cmd=s'             => \$cmd,
 'cli_cmd=s'         => \$cli_cmd,
 'manager|mgr|m=s'   => \$lfmgr_host,
 'manager_port|mgr_port|lf_port|mp:i' => \$lfmgr_port,
 'load_db|load=s'    => \$load,
 'quiet|q=s'         => \$::quiet,
 'resource|card|res|r=i' => \$card,
 'amt_resets=i'      => \$amt_resets,
 'max_port_name=i'   => \$max_port_name,
 'min_sleep=i'       => \$min_sleep,
 'max_sleep=i'       => \$max_sleep,
 'passwd=s'          => \$passwd,
 'set_ifstate|s=s'   => \$if_state,
 'set_speed=s'       => \$set_speed,
 'set_channel=s'     => \$set_channel,
 'set_nss=s'         => \$set_nss,
 'ssid=s'            => \$ssid,
 'list_port_names!'  => \$list_port_names,
 'list_ports!'       => \$list_ports,
 'filter_ports|filter|f=s' => \$filter_ports,
 'show_port:s'       => \$show_port,
 'stats_from_file=s' => \$stats_from_file,
 'port_stats=s{1,}'  => \@port_stats,
 'eap_identity|eapid=s'  => \$eap_identity,
 'eap_passwd|p=s'    => \$eap_passwd,
 'ip=s'              => \$ip,
 'netmask=s'         => \$netmask,
 'gw=s'              => \$gw,
 'log_file|l=s'      => \$log_file,
 'log_cli=s{0,1}'    => \$log_cli,
 'wifi_mode=i'       => \$wifi_mode,
 ) || (print($usage) && exit(1));

 if ($::quiet eq "0") {
   $::quiet = "no";
 }
 elsif ($::quiet eq "1") {
   $::quiet = "yes";
 }

if ($show_help) {
   print $usage;
   exit 0
}

if ($set_nss ne "NA") {
   # Convert to what LANforge CLI wants.
   if ($set_nss eq "2") {
      $set_nss = "4";
   }
   elsif ($set_nss eq "3") {
      $set_nss = "7";
   }
   elsif ($set_nss eq "4") {
      $set_nss = "8";
   }
}

our $utils = undef;
my $t = undef;

if ($stats_from_file eq "") {
  # Open connection to the LANforge server.
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

  # Open connection to the LANforge server.
  my $dt = "";

  # Configure our utils.
  $::utils = new LANforge::Utils();
  my $t = $::utils->connect($lfmgr_host, $lfmgr_port);
  $::utils->sleep_ms(10);
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
} # ~if stats_from_file


if (defined $log_file && ($log_file ne "")) {
   open(CMD_LOG, ">$log_file") or die("Can't open $log_file for writing...\n");
   $cmd_log_name = $log_file;
   if (!$::utils->isQuiet()) {
      print "History of all commands can be found in $log_file\n";
   }
}


sub fmt_port_up_down {
   my ($resource, $port_id, $state) = @_;

   my $cur_flags        = 0;
   if ($state eq "down") {
      $cur_flags        |= 0x1;       # port down
   }

   # Specify the interest flags so LANforge knows which flag bits to pay attention to.
   my $ist_flags        = 0;
   $ist_flags           |= 0x2;       # check current flags
   $ist_flags           |= 0x800000;  # port down

   my $cmd = $::utils->fmt_cmd("set_port", 1, $resource, $port_id, "NA",
           "NA", "NA", "NA", "$cur_flags",
           "NA", "NA", "NA", "NA", "$ist_flags");
   return $cmd;
}

sub fmt_port_ip {
   my ($resource, $port_id, $ip, $mask, $gw) = @_;

   my $set_ip = "NA";
   my $set_mask = "NA";
   my $set_gw = "NA";

   my $ist_flags        = 0;
   $ist_flags        |= 0x4000;       # interested in dhcp

   # Specify the interest flags so LANforge knows which flag bits to pay attention to.
   my $cur_flags        = 0;
   if ($ip eq "DHCP") {
     $cur_flags  |= 0x80000000;
   }
   else {
     $set_ip = $ip;
     $set_mask = $mask;
     $set_gw = $gw;

     if ($set_ip ne "NA") {
       $ist_flags        |= (1<<2);       # interested in IP
     }
     if ($set_mask ne "NA") {
       $ist_flags        |= (1<<3);       # interested in netmask
     }
     if ($set_gw ne "NA") {
       $ist_flags        |= (1<<4);       # interested in gateway
     }
   }

   my $cmd = $::utils->fmt_cmd("set_port", 1, $resource, $port_id, "$set_ip",
                "$set_mask", "$set_gw", "NA", "$cur_flags",
                "NA", "NA", "NA", "NA", "$ist_flags");
   return $cmd;
}

sub fmt_wifi_extra {
   my ($resource, $port_id, $eap_id, $eap_passwd) = @_;
   my $cmd = $::utils->fmt_cmd("set_wifi_extra", 1, $resource, $port_id,
      "NA",    # key_mgmt Key management: WPA-PSK, WPA-EAP, IEEE8021X, NONE, WPA-PSK-SHA256, WPA-EAP-SHA256 or combo.
      "NA",    # pairwise Pairwise ciphers: CCMP, TKIP, NONE, or combination.
      "NA",    # group  Group cyphers: CCMP, TKIP, WEP104, WEP40, or combination.
      "NA",    #  psk WPA pre-shared key.
      "NA",    #  key WEP key0.  Should enter this in ascii-hex.
      "NA",    #  ca_cert CA-CERT file name.
      "NA",    #  eap EAP method: MD5, MSCHAPV2, OTP, GTC, TLS, PEAP, TTLS.
      "$eap_id", #  identity EAP Identity string.
      "NA",    #  anonymous_identity Anonymous identity string for EAP.
      "NA",    #  phase1 Outer-authentication, ie TLS tunnel parameters.
      "NA",    #  phase2 Inner authentication with TLS tunnel.
      "$eap_passwd", #  password EAP Password string.
      "NA",    #  pin EAP-SIM pin string. (For AP, this field is HS20 Operating Class)
      "NA",    #  pac_file EAP-FAST PAC-File name. (For AP, this field is the RADIUS secret password)
      "NA",    #  private_key EAP private key certificate file name. (For AP, this field is HS20 WAN Metrics)
      "NA",    #  pk_passwd EAP private key password. (For AP, this field is HS20 connection capability)
      "NA",    #  hessid 802.11u HESSID (MAC address format).
      "NA",    #  realm 802.11u realm: mytelco.com
      "NA",    #  client_cert 802.11u Client cert file /etc/wpa_supplicant/ca.pem
      "NA",    #  imsi 802.11u IMSI:  310026-000000000
      "NA",    #  milenage 802.11u milenage:  90dca4eda45b53cf0f12d7c9c3bc6a89:cb9cccc4b9258e6dca4760379fb82
      "NA",    #  domain 802.11u domain:  mytelco.com
      "NA",    #  roaming_consortium 802.11u roaming consortium: 223344 (15 characters max)
      "NA",    #  venue_group 802.11u Venue Group, integer. VAP only.
      "NA",    #  venue_type 802.11u Venue Type, integer.  VAP only.
      "NA",    #  network_type 802.11u network type, integer, VAP only.*
      "NA",    #  ipaddr_type_avail 802.11u network type available, integer, VAP only.
      "NA",    #  network_auth_type 802.11u network authentication type, VAP only.
      "NA"    #  anqp_3gpp_cell_net 802.11u 3GCPP Cellular Network Info, VAP only.
      );
   return $cmd;
}

# $::utils->doCmd("log_level 63");

if ($cli_cmd ne "") {
   print $::utils->doAsyncCmd($cli_cmd) ."\n";
   close(CMD_LOG);
   exit(0);
}

if ($load ne "") {
   $cli_cmd = "load $load overwrite";
   my @rslt = $::utils->doAsyncCmd($cli_cmd);
   # $t->waitfor("/LOAD-DB:  Load attempt has been completed./");
   if (!$::utils->isQuiet()) {
      print @rslt;
      print "\n";
   }
   close(CMD_LOG);
   exit(0);
}


if ((defined $list_port_names) && ($list_port_names ne "")) {
   my @lines =split("\n", $::utils->doAsyncCmd("nc_show_ports 1 $card all"));
   my $note = "";
   my $eid = "";
   my $ip = "";
   my @out = ();
   for my $line (@lines) {
      if ($line =~ /^Shelf: 1, /) {
         my ($r, $n) = ($line =~ /Card: (\d+), Port: (\d+) /);
         $eid .="1.${r}.${n} ";
      }
      if ($line =~ / IP: /) {
         my ($i) = ($line =~ / IP: ([^ ]+) /);
         $ip .=" $i";
      }
      if ($line =~ / MAC: .* DEV: /) {
         my ($mac, $dev) = ($line =~ / MAC: ([^ ]+)\s*DEV: ([^ ]+) /);
         push(@out, "$eid\t$dev\t$mac\t$ip");
         $eid = "";
         $ip = "";
      }
   }

   if (@out > 0) {
      print("EID\tDEV\tMAC               \tIP\n");
      print (join("\n", sort(@out))."\n");
   }
   exit(0);
}

if ((defined $filter_ports) && ($filter_ports ne "")) {
   my @lines =split("\n", $::utils->doAsyncCmd("nc_show_ports 1 $card all"));
   my @keys = split(/,/, $filter_ports);
   my $note = "";
   my $eid = "";
   my $next_eid = "";
   my $ip = "";
   my @out = ();
   my $dev = "";
   my %matches = ();
   for(my $i=0; $i <= $#keys; $i++) {
      $keys[$i] =~ tr/ |-/./;
   }
   my $pattern =join("|", @keys);
   my $pattern_la = "(?=".join("|", @keys).": )";
   my $pattern_lb = "(?<  |, |$)";

   for my $line (@lines) {
      my $saw_shelf = 0;
      if ($line =~ /^Shelf: 1, /) {
         $saw_shelf = 1;
         my ($r, $p) = ($line =~ /Card: (\d+), Port: (\d+) /);
         $next_eid ="1.${r}.${p}";
      }
      print "Looking for $pattern in $line\n";
      if ($line =~ / (${pattern}): /i) {
         for my $k (@keys) {
            if (my ($m) = ($line =~ / (?:${k}): ([^ ]+)/i)) {
               $matches{$k} = $m;
            }
         }
      }
      if ($line =~ / MAC: .* DEV: /) {
         ($dev) = ($line =~ / DEV: ([^ ]+) /);
      }
      if ($saw_shelf == 1) {
         if (keys(%matches) > 0) {
            for my $k (sort keys(%matches)) {
               $note .="; " if ($note ne "");
               $note .= "$k: $matches{$k}";
            }
            push(@out, "$eid\t$dev\t$note");
            %matches = ();
         }
         $eid = $next_eid;
         $dev = "";
         $note = "";
         $saw_shelf = 0;
      }
   }

   if (@out > 0) {
      print("EID\tDEV\t".join("\t", @keys)."\n");
      print (join("\n", sort(@out))."\n");
   }
   exit(0);
}

if ((defined $list_ports) && ($list_ports ne "")) {
   print $::utils->doAsyncCmd("nc_show_ports 1 $card all");
   exit(0);
}

if (length($port_name) == 0) {
   print "ERROR:  Must specify port name.\n";
   die("$usage");
}

# this is the --show_port options ("")
if (($show_port ne "NA") && (($show_port eq "1") || ($show_port eq ""))) {
   #$::quiet = 0;
   #$::utils->cli_rcv_silent(0);
   print $::utils->doAsyncCmd("nc_show_port 1 $card $port_name") . "\n";
   exit(0);
}
# this is the --show_port "ssss" options (key,key,key)
elsif(($show_port ne "NA") && ($show_port ne "")) {
   my %option_map    = ();
   my $option        = '';
   for $option (split(',', $show_port)) {
      #print "preprare option_map.$option to ''\n";
      $option="DNS-Servers"      if ($option eq "DNS Servers");
      $option="TX-Queue-Len"     if ($option eq "TX Queue Len");
      $option="Missed-Beacons"   if ($option eq "Missed Beacons");
      $option_map{ $option } = '';
   }
   my $i;
   my @lines = ();
   if ($stats_from_file ne "") {
     @lines = split("\n", get_stats_from_file($stats_from_file, 1, $card, $port_name));
   }
   else {
     @lines = split("\n", $::utils->doAsyncCmd("nc_show_port 1 $card $port_name"));
   }

   my $rh_value_map = $::utils->show_as_hash(\@lines, 1);

   for my $option (keys %option_map) {
      my $val = '-';

      if (defined $rh_value_map->{$option}) {
         $val = $rh_value_map->{$option};

         $option_map{"$option"} = $val;

         if (defined $rh_value_map->{"Cfg-$option"}) {
            $val = $rh_value_map->{"Cfg-$option"};
            $option_map{"Cfg-$option"} = $val;
         }
         if (defined $rh_value_map->{"Probed-$option"}) {
            $val = $rh_value_map->{"Probed-$option"};
            $option_map{"Probed-$option"} = $val;
         }
      }
   }


   for $option ( sort keys %option_map ) {
      #print("Checking option: $option\n");
      print $option.": ".$option_map{ $option }."\n";
   }

   exit(0);
}

if ($if_state ne "unset") {
  if ($if_state eq "up" || $if_state eq "down") {
    $cli_cmd = fmt_port_up_down($card, $port_name, $if_state);
    $::utils->doCmd($cli_cmd);
  }
  else {
    print "ERROR:  ifstate must be 'up' or 'down', value was: $if_state.\n";
    exit (1);
  }
}

if ($set_speed ne "NA" || $ssid ne "NA" || $passwd ne "NA" || $ap ne "NA") {
  $cli_cmd = "add_vsta 1 $card NA $port_name NA '$ssid' NA '$passwd' '$ap' NA NA $wifi_mode '$set_speed'";
  $::utils->doCmd($cli_cmd);
}

if (($set_channel ne "NA") || ($set_nss ne "NA")) {
  $cli_cmd = "set_wifi_radio 1 $card $port_name NA $set_channel NA NA NA NA NA NA NA $set_nss";
  $::utils->doCmd($cli_cmd);
}

if ($eap_identity ne "NA" || $eap_passwd ne "NA") {
   my $cli_cmd = fmt_wifi_extra( $card, $port_name, "$eap_identity", "$eap_passwd");
   $::utils->doCmd($cli_cmd);
}

if ($ip ne "NA") {
   my $cli_cmd = fmt_port_ip( $card, $port_name, $ip, $netmask, $gw);
   $::utils->doCmd($cli_cmd);
}

if ($cmd eq "reset") {
   my $pn_int = -1;
   if ($port_name =~ /^\d+$/ ) {
      $pn_int = int($port_name);
   }
   while (1) {
      my $pname = $port_name;
      if (($pn_int > 0) && ($pn_int < $max_port_name)) {
         $pname = $pn_int + int(rand($max_port_name - $pn_int));
      }
      print("Resetting port: ${shelf_num}.${card}.${pname}\n");
      $cli_cmd = "reset_port $shelf_num $card $pname";
      $::utils->doCmd($cli_cmd);
      $amt_resets_sofar++;
      if ($amt_resets != 0) {
         if ($amt_resets_sofar >= $amt_resets) {
            print("Completed: $amt_resets_sofar resets, exiting.\n");
            close(CMD_LOG);
            exit(0);
         }
      }
      my $sleep_time = $min_sleep;
      if ($min_sleep < $max_sleep) {
         $sleep_time += int(rand($max_sleep - $min_sleep));
      }
      if ($sleep_time > 0) {
         print("Sleeping for: $sleep_time seconds before next reset.\n");
         sleep($sleep_time);
      }
  }#while
}

if ($cmd eq "delete") {
  print("Deleting port: ${shelf_num}.${card}.${port_name}\n");
  $cli_cmd = "rm_vlan $shelf_num $card $port_name";
  $::utils->doCmd($cli_cmd);
}

close(CMD_LOG);
exit(0);


sub get_stats_from_file {
  my $fname = shift;
  my $shelf = shift;
  my $resource = shift;
  my $port_name = shift;

  open(F, "<$fname") or die("Can't open $fname for reading: $!\n");

  my $port_text = "";
  my $s = -1;
  my $c = -1;
  my $p = -1;

  my @lines = ();
  while ( my $line = <F>) {
    @lines = (@lines, $line);
  }
  # Append dummy line to make it easier to terminate the parse logic.
  @lines = (@lines, "Shelf: 9999, Card: 9999, Port: 9999  Type: STA  Alias: \n");

  my $i;
  for ($i = 0; $i<@lines;$i++) {
    my $line = $lines[$i];
    chomp($line);
    if ($line =~ /Shelf:\s+(\d+).*Card:\s+(\d+).*Port:\s+(\d+)/) {
      my $m1 = $1;
      my $m2 = $2;
      my $m3 = $3;

      if ($port_text ne "") {
   # See if existing port entry matches?
   if ($s == $shelf && $c == $resource) {
     my $pname = "";
     my $palias = "";
     if ($port_text =~ /\s+DEV:\s+(\S+)/) {
       $pname = $1;
     }
     if ($port_text =~ /\s+Alias:\s+(\S+)/) {
       $palias = $1;
     }
     #print("search for port_name: $port_name p: $p  palias: $palias  pname: $pname\n");
     if (("$p" eq $port_name) ||
         ($palias eq $port_name) ||
         ($pname eq $port_name)) {
       return $port_text;
     }
   }
      }

      $port_text = "$line\n";
      $s = $m1;
      $c = $m2;
      $p = $m3;
    }
    else {
      if ($port_text ne "") {
   $port_text .= "$line\n";
      }
    }
  }
  return "";
}
