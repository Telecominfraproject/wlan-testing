#!/usr/bin/perl -w
use strict;
use warnings;
use diagnostics;
use Carp;
$SIG{ __DIE__  } = sub { Carp::confess( @_ ) };
$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };

# Un-buffer output
$| = 1;
use Getopt::Long;
use JSON::XS;
use HTTP::Request;
use LWP;
use LWP::UserAgent;
use Data::Dumper;
use Time::HiRes qw(usleep);
use JSON;
use lib '/home/lanforge/scripts';
use LANforge::JsonUtils qw(logg err json_request get_links_from get_thru json_post get_port_names flatten_list);

package main;
# Default values for ye ole cmd-line args.
our $Resource  = 1;
our $quiet     = "yes";
our $Host      = "localhost";
our $Port      = 8080;
our $HostUri   = "http://$Host:$Port";
our $Web       = LWP::UserAgent->new;
our $Decoder   = JSON->new->utf8;
our $ssid;
our $security;
our $passphrase;

my $usage = qq("$0 --host {ip or hostname} # connect to this
   --port {port number} # defaults to 8080
);


my $des_resource = 1;

GetOptions
(
  'host=s'        => \$::Host,
  'port=i'        => \$::Port,
  'resource=i'    => \$des_resource
) || (print($usage) && exit(1));

$::HostUri = "http://$Host:$Port";

my $uri = "/stations/list";
my $rh = json_request($uri);
my $ra_links = get_links_from($rh, 'stations');
# print(Dumper($ra_links));

my @attribs = ("ap", "signal", "tx rate", "rx rate", "capabilities");
for my $sta_uri (@$ra_links) {
    my $with_fields = "$sta_uri?fields=station+bssid,capabilities,rx+rate,tx+rate,signal,ap";
    $rh = json_request($with_fields);
    #print(Dumper($rh));
    #print(Dumper($rh->{station}));
    print("Station ", $rh->{station}->{'station bssid'}, "\n");
    for my $k (@attribs) {
        print("    $k:      ".$rh->{station}->{$k}."\n");
    }
    print("\n");
}



