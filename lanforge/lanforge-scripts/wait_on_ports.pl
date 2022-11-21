#!/usr/bin/perl -w
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ##
## Use this script wait on list of ports until they are up                 ##
## ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ##
use strict;
use warnings;
use diagnostics;
use Data::Dumper;

$| = 1;
use Net::Telnet ();
use LANforge::Utils;
use Getopt::Long;

package main;
# if number of ports to probe is greater than this, probe all ports on card
# so as to reduce chance of timeout
our $batch_thresh = 3;
# if caching_ok > 0, use a c_show_port to get older results faster
our $use_caching  = -1;
our $card         = 1; # resource id
my $mgr           = "localhost";
my $mgr_port      = "4001";
our @port_list    = ();
our $quiet        = 1;
our $require_ip   = 1;
our $verbose      = -1;
our %down_count   = ();
our $shove_level  = 4; # count at which a lf_portmod trigger gets called

sub help() {
   print "$0 --mgr      # manager [$mgr] [default values] in brackets \\
      --mgr_port              # manager port [$mgr_port] \\
      --resource|resrc|card   # resource id [$card] \\
      --quiet yes|no|0|1      # show CLI protocol [$::quiet] \\
      --require_ip 0|1        # require a port to have an IP to be 'up' [$require_ip] \\
      --shove_level           # retry up/down ports [$shove_level] \\
      --verbose 0|1+          # debugging output  [$verbose] \\
      --batch_level           # query all port statuses if querying more than this many [$batch_thresh] \\
      --use_caching 0|1       # faster to use older port status [$use_caching] \\
      --port sta1 -p sta2 -p sta3... \\
      --help|-h \n";
}

if (@ARGV < 1) {
   help();
   exit 0;
}


# should move to Utils
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

my $show_help = 0;
my $p = new Getopt::Long::Parser;
$p->configure('pass_through');

GetOptions (
   'mgr:s'           => \$mgr,
   'mgr_port:i'      => \$mgr_port,
   'card|resource:i' => \$::card,
   'quiet|q:s'       => \$::quiet,
   'ports|p:s@'      => \@::port_list,
   'require_ip:i'    => \$::require_ip,
   'batch_level:i'   => \$::batch_thresh,
   'use_caching:i'   => \$::use_caching,
   'shove_level:i'   => \$::shove_level,
   'v:i'             => \$::verbose,
   'help|h'          => \$show_help,
) || die help();

if ($show_help) {
   help();
   exit 0;
}
if ($::quiet eq "0") {
   $::quiet = "no";
}
elsif ($::quiet eq "1") {
   $::quiet = "yes";
}

my $t = new Net::Telnet(
   Prompt   => '/default\@btbits\>\>/',
   Timeout  => 20);

$t->open(Host => $mgr,
      Port    => $mgr_port,
      Timeout => 10);

$t->waitfor("/btbits\>\>/");
# Configure our utils.
our $utils = new LANforge::Utils();
$::utils->telnet($t);
$::utils{'quiet'} = $::quiet;
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

die("No resource defined, bye.") if (! defined $card);
my $num_ports_down = @::port_list;
if ($verbose > 2) {
   print "\nWe have ".(0+@::port_list)." ports: ".join(",", sort @::port_list), "\n";
}

# performance and timeouts: just probing a port or two is pretty easy, but repeatedly calling nc_show_port
# can chance a timeout, which is pretty messy. Setting a batch-level threshold to check nc_show_port 1 $c ALL
# should reduce chances of timeout

sub query_show_port {
   my $port = shift;
   if (!defined $port || "$port" eq "") {
      die("query_show_port called without port argument");
   }
   my $statblock = "";
   if (($::use_caching < 0) && (@::port_list > (2 * $::batch_thresh))) {
      print STDERR "Turning on use_caching at 2x batch threshold\n";
      $::use_caching = 1;
   }
   my $show = ($::use_caching > 0) ? "c_show_port" : "nc_show_port";

   if (@::port_list < $::batch_thresh) {
      $statblock = $utils->doAsyncCmd($utils->fmt_cmd($show, 1, $::card, $port, "16"));
   }
   else {
      $statblock = $utils->doAsyncCmd($utils->fmt_cmd($show, 1, $::card, 'all', "16"));
   }
   my @blocklines = split("\n", $statblock);
   chomp @blocklines;
   return @blocklines;
}

=pod
expects arg1 $portname
expects arg2 @$ra_statblock to parse
expects arg3 %$rh_hashref
   arg3 hash of {portname => {state=>x, ip=>y}}

We find a port by this type of pattern:
Alias: is not populated unless there is a user alias override set.
Record ends with an empty line.
---------------------------------------------
Shelf: 1, Card: 2, Port: 8  Type: STA  Alias:
 .*
   MAC: 00:0e:8e:54:42:62  DEV: sta2100 .*

---------------------------------------------
=cut
sub parse_show_port {
   my $portname  = shift;
   my $ra_statblock = shift;
   my $rh_port_stat = shift;

   die ("parse_show_port: called without arg1:portname")
      if (!defined $portname || "$portname" eq "");
   die ("parse_show_port: called without arg2:statblock")
      if (!defined $ra_statblock || ref($ra_statblock) ne "ARRAY");
   die ("parse_show_port: called without arg3: rh_port_stat")
      if (!defined $rh_port_stat || ref($rh_port_stat) ne "HASH");

   #for my $line (@$ra_statblock) {
   #   print "\nL: $line";
   #}

   print " $portname " if ($verbose > 3);

   my $state = "";
   my $ip   = "";
   my (@devicelines) = grep {/^\s+MAC: [^ ]+\s+DEV: [^ ]+ /} @$ra_statblock;
   if (@devicelines < 1) {
      print STDERR "device $portname not found\n";
      $rh_port_stat->{'state'} = $state;
      $rh_port_stat->{'ip'} = $ip;
      return;
   }

   # loop through statblock and grep regions divided by blank lines
   my @current_region = ();
   for my $line (@$ra_statblock) {
      if ($line =~ /^Shelf: 1, Card:/) {
         @current_region = ();
      }
      push (@current_region, $line);

      if ($line =~ /^\s*$/) {
         @devicelines = grep {/^\s+MAC: [^ ]+\s+DEV:\s+$portname\s+ /} @current_region;
         next
            if (@devicelines < 1);

         print join("\nDEV| ", @current_region)."\n"
            if ($::verbose > 3) ;

         my (@state) = grep {/^\s+Current:\s+([^ ]+)/} @current_region;
         print join("\nState: ", @state)."\n"
            if ($::verbose > 3);

        ($state) = $state[0] =~ /^\s+Current:\s+([^ ]+)/
            if (@state > 0);

         my (@ip)    = grep {/^\s+IP:\s+([^ ]+)/} @current_region;
         print join("\nIP: ", @ip)."\n"
            if ($::verbose > 3);

         ($ip) = $ip[0] =~ /^\s+IP:\s+([^ ]+)/
            if (@ip > 0);

         last;
      } # ~if at end of record
   } #~for each line

   # retro below
   if (! defined $state) {
      print "STATE undefined: -- \n"; 
   }
   if (! defined $ip) {
      print "IP undefined: -- \n"; 
   }

   $rh_port_stat->{'state'} = $state;
   $rh_port_stat->{'ip'} = $ip;
}

my %port_stat = (
   'state'  => 0,
   'ip'     => "",
);

while( $num_ports_down > 0 ) {
   my @ports_up = ();
   my @ports_down = ();
   my @statblock = ();

   for my $port (sort @::port_list) {
      if (@::port_list < $::batch_thresh) {
         @statblock = query_show_port($port);
      }
      elsif (@statblock < 2) {
         @statblock = query_show_port("all");
      }

      parse_show_port($port, \@statblock, \%port_stat);

      print Dumper(\%port_stat)."\n"
         if ($::verbose > 3);

      if ($require_ip) {
         if (($port_stat{'state'} !~ /down/i) && ($port_stat{'ip'} !~ /0\.0\.0\.0/)) {
            $num_ports_down--;
            push(@ports_up, $port);
            print "+" if ($verbose > 0);
            $down_count{$port} = 0;
         }
         else {
            print "-" if ($verbose > 0);
            push(@ports_down, $port);
            $down_count{$port}++;
         }
      }
      else {
         if ($port_stat{'state'} =~ /down/i) {
            push(@ports_down, $port);
            print "-" if ($verbose > 0);
            $down_count{$port}++;
         }
         else {
            $num_ports_down--;
            print "=" if ($verbose > 0);
            push(@ports_up, $port);
            $down_count{$port} = 0;
         }
      }
   } # ~for each port 

   if ($verbose > 1) {
      my $num_ports = @::port_list;
      my $num_ports_up = @ports_up;
      print "\n\n${num_ports_up}/${num_ports}  Ports up:   ".join(", ", @ports_up   )."\n"
         if ($verbose > 2);
      print "\n${num_ports_down}/${num_ports} Ports down: ".join(", ", @ports_down )."\n";
   }
   if ($num_ports_down > 0) {
      for my $port (sort keys %down_count) {
         my $strikes = $down_count{$port};
         if ($strikes >= $shove_level) {
            print "Shoving port $port\n";
            my $cli_cmd = fmt_port_up_down($card, $port, "down");
            $utils->doCmd($cli_cmd);
            sleep(0.5);
            $cli_cmd = fmt_port_up_down($card, $port, "up");
            $utils->doCmd($cli_cmd);
            $down_count{$port} = 0;
         }
      }
      $num_ports_down = @::port_list;
      @statblock = ();
      print " ";
      print "Napping...\n" if ($verbose > 1);
      sleep 4;
   }
} # ~while num_ports_down > 0

print "All ports up.\n" if ($verbose > 0);
#
