#!/usr/bin/perl -w
use strict;
use warnings;
use diagnostics;
use Carp;
use Time::HiRes qw(usleep);
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
use JSON;
use lib '/home/lanforge/scripts';
use lib "../";
use lib "./";
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

my $usage = qq("$0 --host {ip or hostname} # connect to this
   --port {port number} # defaults to 8080
);


##
##    M A I N
##

GetOptions
(
  'host=s'                   => \$::Host,
  'port=i'                   => \$::Port,
) || (print($usage) && exit(1));

$::HostUri = "http://$Host:$Port";
my $rh_update = {
   'shelf'=>1, 'resource'=>1, 'port'=>'all', 'probe_flags'=>'0x9'
};
my $uri = "/shelf/1";
my $rh = json_request($uri);
my $ra_links = get_links_from($rh, 'resources');
my @links2= ();
my $ra_alias_links = [];
logg("\nRefreshing after setting up... ");
my $rh_response =  json_post("/cli-json/nc_show_ports", $rh_update);

# wait on ports up
my $ports_still_down = 1;
while ($ports_still_down > 0) {
   $rh = json_request("/port/1/1/list?fields=_links,port,device,down");
   flatten_list($rh, 'interfaces');
   $ports_still_down=0;
   for my $rh_p (values %{$rh->{'flat_list'}}) {
      next unless $rh_p->{'device'} =~ /^sta/;
      #print "$rh_p->{'device'} is $rh_p->{'down'} ";
      $ports_still_down++
         if ($rh_p->{'down'});
   }
   print "ports down: $ports_still_down ";
   $rh_response =  json_post("/cli-json/nc_show_ports", $rh_update);
   sleep 1;
}

#
