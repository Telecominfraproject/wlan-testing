#!/usr/bin/perl -w
#-----------------------------------------------------------------------#
# This program is used to create layer-4 connections with               #
# IP4 addresses correlated to username/password combinations            #
# and get some basic information from LANforge.                         #
#                                                                       #
# Written by Candela Technologies Inc.                                  #
#-----------------------------------------------------------------------#
package main;
use strict;
use warnings;
use Carp;
$| = 1;# Un-buffer output

# use lib prepends to @INC, so put lower priority first
# This is before run-time, so cannot condition this with normal 'if' logic.
use lib '/home/lanforge/scripts';
use lib "./";

use Getopt::Long;
use LANforge::Endpoint;
use LANforge::Port;
use LANforge::Utils;
use Net::Telnet ();
use POSIX;
use constant      NA          => "NA";
use constant      NL          => "\n";
use constant      shelf_num   => 1;

# Default values for ye ole cmd-line args.
our $quiet           ="yes";
our $resource        = 1;
our $lfmgr_host      = "localhost";
our $lfmgr_port      = 4001;
our $report_timer    = 5000;
our $outfile_pref    = "l4-out";
our $l4timeout       = 1000 * 60 * 1; # minutes
our $url_rate        = 600;   # urls/10min
our $test_mgr        = "l4_connections";
our $port_range      = undef;
our $auth_pref       = undef;
our $target_url      = undef;
our $port_name       = undef;
our $first_port      = undef;
our $last_port       = undef;
our $user_pref       = undef;
our $pass_pref       = undef;

#-----------------------------------------------------------------------#
#  Nothing to configure below here, most likely.                        #
#-----------------------------------------------------------------------#

our $usage = "\nUsage: $0  --mgr {host-name | IP}
   --mgr_port {ip port}
   --resource {number}
   --report_timer {milliseconds}
   --quiet  {yes|no}
   --timeout {millis}                  # url timeout in milliseconds ($::l4timeout ms)
   --url_rate {per 10 min)             # requests per 10 minutes ($::url_rate)
   --port_range {first-last}           # eg rd0#0-rd0#99 < keep name short!
   --auth_pref {1-4 chars,1-4 chars}   # u,p appended with last octet: u101 p101
   --target_url {http://hostname/path} # http(s) urls will be rewritten to
                  #   http://hostname/path?user=u&pass=p
   --outfile_pref {l4-out} # found in /home/lanforge/l4logs

Example:

 $0 --port_range rd2#0-rd2#99 --auth_pref u,p \
      --target_url 'http://10.99.0.2/index.html'

 $0 --mgr 192.168.101.1 --mgr_port 4001 --resource 1 \\
      --port_range rd0#0-rd0#25 --report_timer 1000 \\
      --auth_pref bob,pas \\
      --target_url 'https://10.99.0.2/index.html' \\
      --outfile_pref 'req_log' \\
      --url_rate 6000 \\
      --timeout 120000

   (*) first create macvlans with a gateway inside a virtual router
";

GetOptions
(
   'quiet|q=s'          => \$::quiet,
   'mgr|m=s'            => \$::lfmgr_host,
   'mgr_port|p=i'       => \$::lfmgr_port,
   'resource|r=i'       => \$::resource,
   'port_range=s'       => \$::port_range,
   'report_timer=i'     => \$::report_timer,
   'auth_pref|ap=s'     => \$::auth_pref,
   'target_url|u=s'     => \$::target_url,
   'outfile_pref|op=s'  => \$::outfile_pref,
   'timeout|to=i'       => \$::l4timeout,
   'url_rate=i'         => \$::url_rate,
) || die("$::usage");

if (  length($::port_range)   < 1
   || length($::auth_pref)    < 1
   || length($::target_url)   < 1) {
   die( "missing port_range, auth_pref,  or target_url: $::usage");
}
#print "PortRange: $::port_range\n";
($::port_name, $::first_port, $::last_port) = $::port_range =~ /([[:alnum:]]+[^[:alnum:]])(\d+)-[[:alnum:]]+[^[:alnum:]](\d+)/;
#print "PortName[$::port_name] FirstPort[$::first_port] LastPort[$::last_port]\n";
#print "AuthPrefix: $::auth_pref\n";
($::user_pref, $::pass_pref) = $::auth_pref =~ /^\s*(\S+)\s*,\s*(\S+)\s*$/;
#print "UserPrefix[$::user_pref] PassPrefix[$::pass_pref]\n";


if ( !defined($::port_name)   || length($::port_name) < 1
   || !defined($::first_port) || length($::first_port)< 1
   || !defined($::last_port)  || length($::last_port) < 1
   || !defined($::user_pref)  || length($::user_pref) < 1
   || !defined($::pass_pref)  || length($::pass_pref) < 1) {
   die( "missing port_name, first_port, last_port, user_pref, or pass_pref: $::usage");
}

our ($schema, $host, $path) = $::target_url =~ /\s*(https?):\/\/([^\/]+)(\/?.*?)\s*$/;
#print "schema[$schema] host[$host] path[$path]\n";

#----------------------------------------------------------------------#
# Wait up to 20 seconds when requesting info from LANforge.
our $t = new Net::Telnet(Prompt => '/default\@btbits\>\>/',
			               Timeout => 20);
$::t->open( Host    => $::lfmgr_host,
            Port    => $::lfmgr_port,
            Timeout => 10);
$::t->max_buffer_length(8 * 1024 * 1000); # 8 MB buffer
$::t->waitfor("/btbits\>\>/");

#-----------------------------------------------------------------------#
#     compat                                                            #
#-----------------------------------------------------------------------#
if ( !defined *LANforge::Utils::fmt_cmd ) { 
   #*LANforge::Utils::fmt_cmd = sub {
   sub LANforge::Utils::fmt_cmd {
      my $self = shift;
      my $rv;
      for my $hunk (@_) {
         $rv .= ( $hunk =~ / +/) ? "'$hunk' " : "$hunk ";
      }
      chomp $rv;
      return $rv;
   };
}
# Configure our utils.
our $utils = new LANforge::Utils();
$::utils->connect($lfmgr_host, $lfmgr_port);


#-----------------------------------------------------------------------#
# survey ports, complain if they are not present                        #
#-----------------------------------------------------------------------#

our %port_ips     = ();
our %port_quads   = ();
our %port_urls    = ();
our %port_download= ();
our %port_file    = ();
my $method        = 1;
my $match         = '(IP: \S+)\s';
my $tmp_quad;
my $tmp_ip;
for (my $i = $::first_port; $i <= $::last_port; $i++) {
   my $tmp_name = $::port_name.$i;
   my @txt = split(/\n/, $::utils->doAsyncCmd("nc_show_port 1 $::resource $tmp_name"));
   if (my ($matched) = grep(/$match/, @txt)) {
      #print "$::port_name$i: found it: $matched\n";
      ($tmp_ip) = $matched =~ /^\s+IP: ([0-9.]+)\s+MASK.*$/;
      ($tmp_quad) = $matched =~ /^\s+IP: [0-9.]+\.([^. ]+)\s+MASK.*$/;
      #print "tmp_quad $tmp_quad tmp_ip:$tmp_ip\n";
   }
   $::port_quads{$i} = $tmp_quad;
   $::port_ips{$i} = $tmp_ip;
   #print "last_q[$tmp_quad]\n";
}


#-----------------------------------------------------------------------#
#                       M A I N                                         #
#-----------------------------------------------------------------------#
# for every port, build the following items:                            #
#     - url with user:pass                                              #
#     - input file url like "dl $url $outfile-$i                        #
#     - create l4 connection with 'use url file'                        #
#-----------------------------------------------------------------------#

my $l4path="/home/lanforge/l4-urls";
if ( !-d $l4path ) {
   mkdir $l4path || die "cannot make $l4path";
}

our $use_url_file = 1;

for (my $i = $::first_port; $i <= $::last_port; $i++) {
   #print "port_quads:".$i."[".$::port_quads{$i}."]\n";
   my $tmp_quad         = $::port_quads{$i};
   #print "tmp_quad[$tmp_quad]\n";

   # style for basic/auth
   #my $url              = $::schema."://".$::user_pref.$tmp_quad.':'.$::pass_pref.$tmp_quad."@".$::host.$::path;

   #get style
   my $url              = $::schema.'://'.$::host.$::path.'?username='.$::user_pref.$tmp_quad.'&password='.$::pass_pref.$tmp_quad;

   print "url[$url]\n";
   $::port_urls{$i}     = $url;
   $::port_download{$i} = "dl $url $l4path/$outfile_pref-$port_name$i.txt\n";
   $::port_file{$i}     = "$l4path/dl_$port_name$i.txt";
}

my $proxy_server     = NA;
my $proxy_userpwd    = NA;
my $ssl_cert_fname   = "ca-bundle.crt";
my $user_agent       = NA;
my $proxy_auth_type  = "0";
my $http_auth        = 3; # | 0x2; for digest
my $dns_cache_to     = 60; #default
my $max_speed        = 0;
my $block_size       = NA;
my $smtp_from        = NA;

# create test-mgr
my @testmgrs = split(/\n/, $::utils->doCmd("show_tm all"));
if( my($tmmatches) = grep /$::test_mgr/, @testmgrs) {
   #print "test_mgr:$tmmatches\n";
}
else {
   $::utils->doCmd("add_tm $::test_mgr");
}



for (my $i = $::first_port; $i <= $::last_port; $i++) {
   # create dummy endpoint
   my $tmp_ep1 = "L4_$port_name$i";
   my $tmp_ep2 = "D_L4_$port_name$i";
   my $cmd     = $::utils->fmt_cmd( "add_l4_endp", $tmp_ep2, 
                                       shelf_num, $::resource, "$port_name$i", 
                                       "l4_generic", 0, 0, 0, ' ', ' ');
   #print "cmd: $cmd\n";
   $::utils->doCmd($cmd);
   $cmd        = $cmd = "set_endp_flag $tmp_ep2 unmanaged 1";
   #print "cmd: $cmd\n";
   $::utils->doCmd($cmd);
   #sleep(0.2);

   # create live endpoint
   my $ip_addr    = $::port_ips{$i};
   open(my $fh, ">", $::port_file{$i} ) || die "unable to create file $::port_file{$i}";
   print $fh $::port_download{$i};
   close $fh;

   # layer4 endpoint
   my $url     = ($::use_url_file)
                  ? $::port_file{$i}
                  : $::port_download{$i}
                  ;
   $cmd        = $::utils->fmt_cmd( "add_l4_endp", $tmp_ep1,
                                    shelf_num, $::resource, "$port_name$i",
                                    "l4_generic", 0, $::l4timeout, $::url_rate,
                                    $url, $proxy_server, $proxy_userpwd,
                                    $ssl_cert_fname, $user_agent, $proxy_auth_type,
                                    $http_auth, $dns_cache_to, $max_speed, $block_size,
                                    $smtp_from, "AUTO" );
   #print "cmd: $cmd\n";
   $::utils->doCmd($cmd);
   #sleep(0.2);
   if ($::use_url_file) {
      $cmd = $::utils->fmt_cmd("set_endp_flag", "$tmp_ep1", "GetUrlsFromFile", 1);
      $::utils->doCmd($cmd);
      #sleep(0.2);
   }
   #$::utils->doCmd("set_cx_report_timer $::test_mgr $tmp_ep1 $report_timer");
   #sleep(0.2);

   my $cx_name = "CX_$tmp_ep1"; # was CX-L4-
   $cmd        = $::utils->fmt_cmd("add_cx", $cx_name, $test_mgr, $tmp_ep1, $tmp_ep2);
   #print "cmd: $cmd\n";
   $::utils->doCmd($cmd);
   #sleep(0.2);
   $::utils->doCmd("set_cx_report_timer $::test_mgr $cx_name $report_timer");
}

#
