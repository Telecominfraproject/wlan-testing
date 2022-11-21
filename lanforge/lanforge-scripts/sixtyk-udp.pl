#!/usr/bin/perl -w
use strict;
use warnings;

use Carp;
$SIG{__DIE__} = sub { Carp::confess(@_)};
$SIG{__WARN__} = sub { Carp::confess(@_)};

$| = 1;
use lib '/home/lanforge/scripts';
use lib '../';
use lib './';
use LANforge::Utils;

package main;

my $num_connections = 60000;
my $speed = 2400; # 16000;
my $pktsz = "AUTO";
our $lfmgr_host = "localhost";
our $lfmgr_port = 4001;
our $resource = 1;
my $port_a = "r1a";
my $port_b = "r2a";
our $quiet = "yes";
our $utils = new LANforge::Utils();
$utils->connect($main::lfmgr_host, $main::lfmgr_port);

our @connections = ();
my $n = 0;

for (my $c = 1; $c <= $num_connections; $c++) {
    $n = (10 * $num_connections) + $c;
    push(@connections, "tcp".substr("$n", 1));
}

my @cmds = ();
foreach my $con_name (@::connections) {
    @cmds = (
       "add_endp ${con_name}-A 1 1 $port_a lf_udp -1 NO $speed $speed NO $pktsz $pktsz increasing 1",
       "set_endp_report_timer ${con_name}-A 15000",
       #"set_endp_details ${con_name}-A 8912 8912",
       "add_endp ${con_name}-B 1 1 $port_b lf_udp -1 NO $speed $speed NO $pktsz $pktsz increasing 1",
       "set_endp_report_timer ${con_name}-B 15000",
       #"set_endp_details ${con_name}-B 8912 8912",
       "add_cx ${con_name} default_tm ${con_name}-A ${con_name}-B",
       "set_cx_report_timer default_tm ${con_name} 15000 cxonly",
    );
    foreach my $cmd (@cmds) {
        $utils->doCmd($cmd);
        print(".");
    }
    print("0");
}
print("\n");
