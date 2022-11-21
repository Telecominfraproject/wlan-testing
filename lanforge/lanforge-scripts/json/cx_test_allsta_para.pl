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
use JSON;
use Time::HiRes qw(usleep nanosleep);

# using this is going to want high inotify instances, like mentioned here:
# sysctl fs.inotify.max_user_instances=256
# https://forum.proxmox.com/threads/unable-to-create-new-inotify-object-too-many-open-files-at-usr-share-perl5.23700/

use Proc::Background;
use lib '/home/lanforge/scripts';
use lib "../";
use lib "./";
use LANforge::JsonUtils qw(logg err json_request get_links_from get_thru json_post get_port_names);

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


##
##    M A I N
##

GetOptions
(
  'host=s'        => \$::Host,
  'port=i'        => \$::Port
) || (print($usage) && exit(1));

$::HostUri = "http://$Host:$Port";

my $uri = "/shelf/1";
my $rh = json_request($uri);
my $ra_links = get_links_from($rh, 'resources');
my @links2= ();
my $ra_alias_links = [];

my $rh_existing_cx = json_request("/cx/list");

my $rh_existing_cxnames = {};
for my $eid (keys %$rh_existing_cx) {
   next if ($eid !~ /^\d+\.\d+$/);
   print "EID[$eid]:";
   print "=================================================================================\n";
   print Dumper($rh_existing_cx->{$eid});
   print "=================================================================================\n";
   my $rh_cx = $rh_existing_cx->{$eid};
   print Dumper($rh_cx);
   print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==\n";
   my $cx_n = $rh_cx->{'name'};
   print " $cx_n ";
   $rh_existing_cxnames->{$cx_n} = $rh_cx;
}
# $SIG{'CHLD'} = "wait_for_child_to_die"; # do we need this?

my @pids=();
for my $cx_name (keys %$rh_existing_cxnames) {
   next if ($cx_name !~ /^udp_/);
   my $proc = Proc::Background->new("./cx_test_helper.pl --cxname $cx_name");
   push(@pids, $proc->pid());
   print " cx_name $cx_name ".$proc->pid();
   usleep(1500);
}

print "...done\n";
#
