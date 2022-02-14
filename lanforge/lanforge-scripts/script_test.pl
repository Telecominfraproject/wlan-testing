#!/usr/bin/perl -w
# This script tests scripts
use strict;
use warnings;
use diagnostics;
use Carp;
use Time::HiRes qw(usleep);
$SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };
$| = 1;

use Net::Telnet;
use lib '.';
use lib './LANforge';
# Ubuntu: libtry-tiny-smartcatch-perlq
use Try::Tiny;
use Getopt::Long;

use HTTP::Request;
use LWP;
use LWP::UserAgent;
require JSON;
require JSON::PP;
use JSON::XS;
use Data::Dumper;
# Ubuntu: libtest2-suite-perl
use Test2::V0 qw(ok fail done_testing is note);
use Test2::Tools::Basic qw(plan);

use constant NA => "NA";
use LANforge::Utils;
use LANforge::Port;
use LANforge::Endpoint;
use LANforge::JsonUtils qw(err logg xpand json_request get_links_from get_thru json_post get_port_names flatten_list);
use LANforge::Test qw(new test run);
#our $PASS = $LANforge::Test::PASS;
#our $FAIL = $LANforge::Test::FAIL;

package main;
our $LFUtils;
our $lfmgr_host       = "ct524-debbie";
our $lfmgr_port       = 4001;
our $http_port        = 4001;
our $resource         = 1;
our $quiet            = 1;
our @specific_tests   = ();
our %test_subs        = ();
our $lf_mgr           = undef;
our $HostUri          = undef;
our $Web              = undef;
our $Decoder          = undef;
our $testport         = "eth1";
#our @test_errs        = ();
my $help              = 0;
my $list              = 0;
my $usage = qq($0 --mgr {lanforge hostname/IP}
  --mgr_port|p {lf socket (4001)}
  --resource|r {resource number (1)}
  --quiet {0,1,yes,no}
  --test|t {test-name} # repeat for test names
  --list|l # list test names
  --testport|tport|tp {$testport}
);

GetOptions (
   'mgr|m=s'            => \$::lfmgr_host,
   'mgr_port|p:s'       => \$::lfmgr_port,
   'card|resource|r:i'  => \$resource,
   'quiet|q:s'          => \$quiet,
   'test|t:s'           => \@specific_tests,
   'help|h'             => \$help,
   'list|l'             => \$list,
   'testport|tport|tp:s' => \$::testport,
) || (print($usage) && exit(1));

if ($help) {
  print($usage) && exit(0);
}

our %tests = ();

$lf_mgr = $lfmgr_host;
$::HostUri   = "http://$lf_mgr:$http_port";
$::Web       = LWP::UserAgent->new;
$::Decoder   = JSON->new->utf8;

my $telnet = new Net::Telnet(Prompt => '/default\@btbits\>\>/',
                       Timeout => 20);
$telnet->open(Host    => $::lf_mgr,
        Port    => $::lfmgr_port,
        Timeout => 10);
$telnet->waitfor("/btbits\>\>/");
$::LFUtils = new LANforge::Utils();
$::LFUtils->telnet($telnet);         # Set our telnet object.
if ($::LFUtils->isQuiet()) {
 if (defined $ENV{'LOG_CLI'} && $ENV{'LOG_CLI'} ne "") {
   $::LFUtils->cli_send_silent(0);
 }
 else {
   $::LFUtils->cli_send_silent(1); # Do not show input to telnet
 }
 $::LFUtils->cli_rcv_silent(1);  # Repress output from telnet
}
else {
 $::LFUtils->cli_send_silent(0); # Show input to telnet
 $::LFUtils->cli_rcv_silent(0);  # Show output from telnet
}

our $port_ip = "";

#----------------------------------------------------------------------
#   Tests
#----------------------------------------------------------------------


#----------------------------------------------------------------------
# multiple ways of querying a port:
# * CLI
# * Port.pm
# * JSON
# * shell out to perl script
#----------------------------------------------------------------------
$tests{'query_port_cli'} = LANforge::Test->new(Name=>'query_port_cli',
   Desc=>'query port using cli', Test => sub{
     my $self = shift;
     my $cmd = $::LFUtils->fmt_cmd("nc_show_port", 1, $::resource, $::testport);
     my $resp = $::LFUtils->doAsyncCmd($cmd);
     my ($mac) = $resp =~ /MAC:\s+([^ ]+)\s+DEV:/;
     ok($mac =~ /:/ );
   });

## test LANforge::Port
$tests{'query_port_class_port'} = LANforge::Test->new(Name=>'query_port_class_port',
   Desc=>'query port using class Port', Test=>sub {
     my $self = shift;
     my $cmd = $::LFUtils->fmt_cmd("nc_show_port", 1, $::resource, $::testport);
     my $resp = $::LFUtils->doAsyncCmd($cmd);
     my $lf_port = LANforge::Port->new;
     $lf_port->decode($resp);
     ok($lf_port->mac_addr() =~ /:/);
   });

## test JsonUtils/port
$tests{'query_port_jsonutils'} = LANforge::Test->new(Name=>'query_port_jsonutils',
   Desc=>'query port using jsonutils', Test=>sub {
      my $self = shift;
      my $url = "http://".$::lf_mgr.":8080/port/1/1/$::testport";
      my $port_json = json_request($url);
      #print Dumper($port_json);
      #ok($port_json->{interface}->{ip} eq $::port_ip);
      ok($port_json->{interface}->{mac} =~ /:/);
   });

## test lf_portmod.pl
$tests{'query_port_lfportmod'} = LANforge::Test->new(Name=>'query_port_lfportmod',
   Desc=>'query port using lfportmod', Test=>sub {
      my $self = shift;
      fail("lf_portmod.pl not found in ".cwd()) if (! -f "./lf_portmod.pl");
      #print "\nTrying: ./lf_portmod.pl --mgr $::lf_mgr --mgr_port $::lfmgr_port --card $::resource --port_name $::testport --show_port\n";
      my $resp = `./lf_portmod.pl --mgr $::lf_mgr --mgr_port $::lfmgr_port --card $::resource --port_name $::testport --show_port`;
      if (length($resp) < 250) {
        note($resp);
        fail("response too short") ;
      }
      my ($mac) = $resp =~ /MAC:\s+([^ ]+)\s+DEV:/;
      ok($mac =~ /:/ );
   });

$tests{'port_down_up_down_cli'} = LANforge::Test->new(Name=>'port_down_up_down_cli',
   Desc=>'port_down_up_down, cli', Test=>sub {
     my $self = shift;
     my $up = 0;
     my $down = 1;
     my $report_timer = 1000; # ms
     my $status = -1;
     my $cmd = $::LFUtils->fmt_cmd("set_port", 1, $::resource, $::testport,
       NA, NA, NA, NA, $down, NA, NA, NA, NA, 8421378, $report_timer);

     my $resp = $::LFUtils->doAsyncCmd($cmd);
     my $begin = time();
     until ($status == $down) {
       sleep 1;
       print ".";
       $resp = $::LFUtils->doAsyncCmd("nc_show_port 1 $resource $::testport");
       my @lines = split("\n", $resp);
       my @matching = grep { /^\s+Current:\s+/ } @lines;
       fail("eth1 has multiple lines starting with Current")
         if (@matching > 1);
       print "Matching Current: $matching[0]\n";
       my ($updown) = $matching[0] =~ /Current:\s+(\w+)\s+/;
       $status = ($updown eq "DOWN") ? $down : (($updown eq "UP") ? $up : -1);
       print $matching[0] if ($status == -1);
       if ((time() - $begin) > 15) {
          note($resp);
          fail("port does not report down in 15 seconds");
       }
     }
     print "port is down\n";
     ok(1);
     sleep 2;

     $cmd = $::LFUtils->fmt_cmd("set_port", 1, $::resource, $::testport,
       NA, NA, NA, NA, $up, NA, NA, NA, NA, 8421378, $report_timer);
     $resp = $::LFUtils->doAsyncCmd($cmd);
     $begin = time();
     until ($status == $up) {
       sleep 1;
       print ".";
       $resp = $::LFUtils->doAsyncCmd("nc_show_port 1 $resource $::testport");
       my @lines = split("\n", $resp);
       my @matching = grep { /^\s+Current:\s+/ } @lines;
       fail("eth1 has multiple lines starting with Current") 
         if (@matching > 1);
       my ($updown) = $matching[0] =~ /Current:\s+(\w+)\s+/;
       $status = ($updown eq "DOWN") ? $down : (($updown eq "UP") ? $up : -1);
       print $matching[0] if ($status == -1);
       if ((time() - $begin) > 15) {
         note($resp);
         fail("port does not report up in 15 seconds");
       }
     }
     print "port is up\n";
     ok(1);
     sleep 2;
     
     $cmd = $::LFUtils->fmt_cmd("set_port", 1, $::resource, $::testport,
       NA, NA, NA, NA, $down, NA, NA, NA, NA, 8421378, $report_timer);
     $resp = $::LFUtils->doAsyncCmd($cmd);
     $begin = time();
     until ($status == $down) {
       sleep 1;
       print ".";
       $resp = $::LFUtils->doAsyncCmd("nc_show_port 1 $resource $::testport");
       my @lines = split("\n", $resp);
       my @matching = grep { /^\s+Current:\s+/ } @lines;
       fail("eth1 has multiple lines starting with Current") 
        if (@matching > 1);
       my ($updown) = $matching[0] =~ /Current:\s+(\w+)\s+/;
       $status = ($updown eq "DOWN") ? $down : (($updown eq "UP") ? $up : -1);
       print $matching[0] if ($status == -1);
       if ((time() - $begin) > 15) {
         note($resp);
         fail("port does not report down in 15 seconds");
       }
     }
     print "port is down\n";
     ok(1);
   });

$tests{'port_down_up_down_class_port'} = LANforge::Test->new(Name=>'port_down_up_down_class_port',
   Desc=>'set port up, class Port', Test=>sub {
   my $self = pop;
   my $report_timer = 1000; # ms
   my $up = 0;
   my $down = 1;
   my $status = -1;
   
   # this class cannot actually manipulate anything and has no commands
   my $resp = $::LFUtils->doAsyncCmd("nc_show_port 1 $resource $::testport");
   my $lfport = LANforge::Port->new;
   $lfport->decode($resp);
   #print ("cur flags: ".$lfport->cur_flags()."\n");
   my $cmd = $::LFUtils->fmt_cmd("set_port", 1, $::resource, $::testport,
     NA, NA, NA, NA, $down, NA, NA, NA, NA, 8421378, $report_timer);

   $resp = $::LFUtils->doAsyncCmd($cmd);
   my $begin = time();
   until ($status == $down) {
     sleep 1;
     print ".";
     $resp = $::LFUtils->doAsyncCmd("nc_show_port 1 $resource $::testport");
     $lfport->decode($resp);
     #print ("cur flags: ".$lfport->cur_flags()."\n");
     my ($updown) = $lfport->cur_flags() =~ /(DOWN|UP)\s+LINK-/;
     $status = ($updown eq "DOWN") ? $down : (($updown eq "UP") ? $up : -1);
     if ((time() - $begin) > 15) {
        note($resp);
        fail("port does not report down in 15 seconds");
     }
   }
   ok($status == $down);
   print "port is down\n";
   sleep 1;
   
   $cmd = $::LFUtils->fmt_cmd("set_port", 1, $::resource, $::testport,
     NA, NA, NA, NA, $up, NA, NA, NA, NA, 8421378, $report_timer);
   $resp = $::LFUtils->doAsyncCmd($cmd);
   $begin = time();
   until ($status == $up) {
     sleep 1;
     print ".";
     $resp = $::LFUtils->doAsyncCmd("nc_show_port 1 $resource eth1");
     $lfport->decode($resp);
     #print ("cur flags: ".$lfport->cur_flags()."\n");
     my ($updown) = $lfport->cur_flags() =~ /(DOWN|UP)\s+LINK-/;
     $status = ($updown eq "DOWN") ? $down : (($updown eq "UP") ? $up : -1);
     if ((time() - $begin) > 15) {
       note($resp);
       fail("port does not report up in 15 seconds");
       last;
     }
   }
   print "port is up\n";
   ok($status == $up);
   sleep 1;

   $cmd = $::LFUtils->fmt_cmd("set_port", 1, $::resource, "eth1",
     NA, NA, NA, NA, $down, NA, NA, NA, NA, 8421378, $report_timer);
   $resp = $::LFUtils->doAsyncCmd($cmd);
   $begin = time();
   until ($status == $down) {
     sleep 1;
     print ".";
     $resp = $::LFUtils->doAsyncCmd("nc_show_port 1 $resource eth1");
     $lfport->decode($resp);
     #print ("cur flags: ".$lfport->cur_flags()."\n");
     my ($updown) = $lfport->cur_flags() =~ /(DOWN|UP)\s+LINK-/;
     $status = ($updown eq "DOWN") ? $down : (($updown eq "UP") ? $up : -1);
     if ((time() - $begin) > 15) {
       note($resp);
       fail("port does not report down in 15 seconds");
       last;
     }
   }
   ok($status == $down);
   print "port is down\n";
   });

$tests{'port_down_up_down_jsonutils'} = LANforge::Test->new(Name=>'port_down_up_down_jsonutils',
   Desc=>'set port up, jsonutils', Test=>sub {
   my $self = shift;
   my $report_timer = 1000; # ms
   my $up = 0;
   my $down = 1;
   my $status = -1;
   my $updown = "";
   my $url = "http://".$::lf_mgr.":8080/port/1/1/$::testport";
   my $rh_data = {
     'shelf'        => 1,
     'resource'     => $::resource,
     'port'         => $::testport,
     'current_flags' => $down,
     'interest'     => 8421378,
     'report_timer' => 1000,
   };
   my $port_json = undef;
   my $rh_response = json_post("http://".$::lf_mgr.":8080/cli-json/set_port", $rh_data);
   my $begin = time();
   my $lfport = LANforge::Port->new;
   until( $status == $down ) {
     sleep 1;
     $port_json = json_request($url);
     my $resp = $::LFUtils->doAsyncCmd("nc_show_port 1 $resource $::testport");
     $lfport->decode($resp);
     #print "$updown <CF: ".$lfport->cur_flags()."\n";
     ($updown) = $lfport->cur_flags() =~ /^\s*(DOWN|UP)\s+/;
     $status = ($port_json->{interface}->{down}) ? $down : (!($port_json->{interface}->{down}) ? $up : -1);
     if ((time() - $begin) > 15) {
        note($resp);
        fail("port does not report down in 15 seconds");
        last;
     }
   }
   print "$updown {CF: ".$lfport->cur_flags()."\n";
   ok($updown eq "DOWN", "$updown {CF: ".$lfport->cur_flags()."\n");
   ok($status == $down, "$updown {CF: ".$lfport->cur_flags()."\n");
   
   $port_json = undef;
   $rh_data->{current_flags} = $up;
   $rh_response = json_post("http://".$::lf_mgr.":8080/cli-json/set_port", $rh_data);
   $begin = time();
   until( $status == $up ) {
     sleep 1;
     $port_json = json_request($url);
     my $lfport = LANforge::Port->new;
     my $resp = $::LFUtils->doAsyncCmd("nc_show_port 1 $resource $::testport");
     $lfport->decode($resp);
     ($updown) = $lfport->cur_flags() =~ /^\s*(DOWN|UP)\s+/;
     #print "$updown <CF: ".$lfport->cur_flags()."\n";
     $status = ($port_json->{interface}->{down}) ? $down : (!($port_json->{interface}->{down}) ? $up : -1);
     if ((time() - $begin) > 15) {
        note($resp);
        fail("port does not report up in 15 seconds");
     }
   }
   ok($updown eq "UP", "$updown {CF: ".$lfport->cur_flags()."\n");
   ok($status == $up, "$updown {CF: ".$lfport->cur_flags()."\n");
   
   $port_json = undef;
   $rh_data->{current_flags} = $down;
   $rh_response = json_post("http://".$::lf_mgr.":8080/cli-json/set_port", $rh_data);
   $begin = time();
   until( $status == $down ) {
     sleep 1;
     $port_json = json_request($url);
     my $lfport = LANforge::Port->new;
     my $resp = $::LFUtils->doAsyncCmd("nc_show_port 1 $resource $::testport");
     $lfport->decode($resp);
     ($updown) = $lfport->cur_flags() =~ /^\s*(DOWN|UP)\s+/;
     #print "$updown <CF: ".$lfport->cur_flags()."\n";
     $status = ($port_json->{interface}->{down}) ? $down : (!($port_json->{interface}->{down}) ? $up : -1);
     last if ($status == $down);
     if ((time() - $begin) > 15) {
        note($resp);
        fail("port does not report down in 15 seconds");
     }
   }
   #print "$updown {CF: ".$lfport->cur_flags()."\n";
   ok($updown eq "DOWN", "$updown {CF: ".$lfport->cur_flags()."\n");
   ok($status == $down, "$updown {CF: ".$lfport->cur_flags()."\n");
  });

$tests{'port_down_up_down_lfportmod'} = LANforge::Test->new(Name=>'port_down_up_down_lfportmod',
   Desc=>'set port up, lfportmod', Test=>sub {
   my $self = shift;
   my $up = 0;
   my $down = 1;
   my $status = -1;
   my $updown = "";
   my $begin = time();
   my $lfport = LANforge::Port->new;
   print "----------------------------------------------\n";
   print "./lf_portmod.pl --mgr $::lf_mgr --mgr_port $::lfmgr_port --card $::resource --port_name $::testport --set_ifstat down\n";
   my $cmd_resp = `./lf_portmod.pl --mgr $::lf_mgr --mgr_port $::lfmgr_port --card $::resource --port_name $::testport --set_ifstat down`;
   print "----------------------------------------------\n";
   until( $status == $down ) {
     sleep 1;
     my $resp = $::LFUtils->doAsyncCmd("nc_show_port 1 $resource $::testport");
     $lfport->decode($resp);
     ($updown) = $lfport->cur_flags() =~ /^\s*(DOWN|UP)\s+/;
     $status = ($updown eq "DOWN") ? $down : (($updown eq "UP") ? $up : -1);
     if ((time() - $begin) > 15) {
        note($resp);
        fail("port does not report down in 15 seconds");
        last;
     }
   }
   #print "$updown {CF: ".$lfport->cur_flags()."\n";
   ok($updown eq "DOWN", "$updown {CF: ".$lfport->cur_flags()."\n");
   ok($status == $down, "$updown {CF: ".$lfport->cur_flags()."\n");
   
   $cmd_resp = `./lf_portmod.pl --mgr $::lf_mgr --mgr_port $::lfmgr_port --card $::resource --port_name $::testport --set_ifstat up`;
   $begin = time();
   until( $status == $up ) {
     sleep 1;
     my $resp = $::LFUtils->doAsyncCmd("nc_show_port 1 $resource $::testport");
     $lfport->decode($resp);
     ($updown) = $lfport->cur_flags() =~ /^\s*(DOWN|UP)\s+/;
     #print "$updown <CF: ".$lfport->cur_flags()."\n";
     $status = ($updown eq "DOWN") ? $down : (($updown eq "UP") ? $up : -1);
     if ((time() - $begin) > 15) {
        note($resp);
        fail("port does not report up in 15 seconds");
     }
   }
   ok($updown eq "UP", "$updown {CF: ".$lfport->cur_flags()."\n");
   ok($status == $up, "$updown {CF: ".$lfport->cur_flags()."\n");
   
   $cmd_resp = `./lf_portmod.pl --mgr $::lf_mgr --mgr_port $::lfmgr_port --card $::resource --port_name $::testport --set_ifstat down`;
   $begin = time();
   until( $status == $down ) {
     sleep 1;
     my $resp = $::LFUtils->doAsyncCmd("nc_show_port 1 $resource $::testport");
     $lfport->decode($resp);
     ($updown) = $lfport->cur_flags() =~ /^\s*(DOWN|UP)\s+/;

     $status = ($updown eq "DOWN") ? $down : (($updown eq "UP") ? $up : -1);
     last if ($status == $down);
     if ((time() - $begin) > 15) {
        note($resp);
        fail("port does not report down in 15 seconds");
     }
   }
   #print "$updown {CF: ".$lfport->cur_flags()."\n";
   ok($updown eq "DOWN", "$updown {CF: ".$lfport->cur_flags()."\n");
   ok($status == $down, "$updown {CF: ".$lfport->cur_flags()."\n");
  });

  
  
sub t_set_port_down {
  ## test CLI
  ## test LANforge::Port
  ## test JsonUtils/port
  ## test lf_portmod.pl
}

sub t_create_mvlan {
  ## test CLI
  ## test LANforge::Port
  ## test JsonUtils/port
  ## test lf_portmod.pl
}

sub t_destroy_mvlan {
  ## test CLI
  ## test LANforge::Port
  ## test JsonUtils/port
  ## test lf_portmod.pl
}

sub t_query_radio {
  ## test CLI
  ## test LANforge::Port
  ## test JsonUtils/port
  ## test lf_portmod.pl
}

sub t_del_all_stations {
  ## test CLI
  ## test LANforge::Port
  ## test JsonUtils/port
  ## test lf_portmod.pl
}

sub t_add_station_to_radio {
  ## test CLI
  ## test LANforge::Port
  ## test JsonUtils/port
  ## test lf_portmod.pl
}

sub t_station_up {
  ## test CLI
  ## test LANforge::Port
  ## test JsonUtils/port
  ## test lf_portmod.pl
}

sub t_station_down {
  ## test CLI
  ## test LANforge::Port
  ## test JsonUtils/port
  ## test lf_portmod.pl
}

sub t_remove_radio {
  ## test CLI
  ## test LANforge::Port
  ## test JsonUtils/port
  ## test lf_portmod.pl
}

sub t_add_sta_L3_udp {
  ## test CLI
  ## test LANforge::Port
  ## test JsonUtils/port
  ## test lf_portmod.pl
}

sub t_sta_L3_start {
  ## test CLI
  ## test LANforge::Port
  ## test JsonUtils/port
  ## test lf_portmod.pl
}

sub t_sta_L3_stop {
  ## test CLI
  ## test LANforge::Port
  ## test JsonUtils/port
  ## test lf_portmod.pl
}

sub t_rm_sta_L3 {
  ## test CLI
  ## test LANforge::Port
  ## test JsonUtils/port
  ## test lf_portmod.pl
}

#----------------------------------------------------------------------
#----------------------------------------------------------------------
our @test_list = (
 'query_port_cli',
 'query_port_class_port',
 'query_port_jsonutils',
 'query_port_lfportmod',
 'port_down_up_down_cli',
 'port_down_up_down_class_port',
 'port_down_up_down_jsonutils',
 'port_down_up_down_lfportmod',
  
  #'03_set_port_down'          => 0,
  #'04_create_mvlan'           => 0,
  #'05_destroy_mvlan'          => 0,
  #'06_query_radio'            => 0,
  #'07_del_all_stations'       => 0,
  #'08_add_station_to_radio'   => 0,
  #'09_station_up'             => 0,
  #'10_station_down'           => 0,
  #'11_remove_radio'           => 0,
  #'12_add_sta_L3_udp'         => 0,
  #'13_sta_L3_start'           => 0,
  #'14_sta_L3_stop'            => 0,
  #'15_rm_sta_L3'              => 0,
);


sub RunTests {
  my $rf_test = undef;
  my @run_these = @::test_list;
  if (@specific_tests > 0) {
    @run_these = (@specific_tests);
  }

  for my $test_name (@run_these) {
    die("test $test_name not found")
      if (! (defined $::tests{$test_name}));

    my $r_test = $::tests{$test_name};
    next if ($r_test == 0);
    try {
      print "$test_name...";
      my $rv = $r_test->test;
      print "$rv\n";
    }
    catch {
      print("Error:".$_ );
    }
  }

}

# ====== ====== ====== ====== ====== ====== ====== ======
#   M A I N
# ====== ====== ====== ====== ====== ====== ====== ======

if ($list) {
  my $av="";
  print "Test names:\n";
  for my $test_name (@::test_list) {
      $av=" ";
      if (defined $::tests{$test_name}) {
         $av='*';
      }
      print " ${av} ${test_name}\n";
  }
  exit(0);
}
else {
  RunTests();
}
#done_testing();
#if (@test_errs > 1) {
#  print "Test errors:\n";
#  print join("\n", @::test_errs);
#}
print "\ndone\n";
#
