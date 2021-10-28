#!/usr/bin/perl
##
## Reads a CSV of attenuator settings and plays them back 
## Remember that 300 is deci-dB; eg 300: sets a channel to 30.0 dB
##
use strict;
use warnings;
use diagnostics;
use Carp;
$SIG{__DIE__} = sub{Carp::confess(@_)};
use Getopt::Long;
use lib '/home/lanforge/scripts';
use Net::Telnet;
use Time::HiRes qw(usleep);
use LANforge::Utils;
use LANforge::csv qw();
$| = 1;

our $usage = qq($0: replay a csv file of attenuator values
   --mgr|m           LANforge manager host
   --file|f          CSV file
   --delay|d         Override of %delay variable, milliseconds between applying rows
   --loop|l          Repeat indefinitely
   --channel|c       Override of channels variable, eg: 1.2.3.1,2.3.4.3
   --minimum|min|i   Set minimum attenuation value (not lower than zero)
   --maximum|max|x   Set maximum attenuation value (not higher than 955)
   --dry_run|dryrun|dry|n    Do not apply attenuation, just parse file, ignore nap times

Example that works on localhost manager:
   $0 --file values.csv

Example that overrides delay to 1600, overrides channels and runs once:
   $0 --mgr 192.168.101.1 --file values.csv --delay 1600  --channel 1.1.3.1,1.1.3.2,1.1.3.3

Example that overrides delay to 600ms, loops forever, and overrides min and max attenuation
   $0 -m 192.168.101.1 -f values.csv -d 600 -l -min 10 -max 900

File Format:
   # < comment lines are ignored
   # 60 milliseconds between rows
   delay,60
   # Directives: DELAY,delay and naptime are equivalent
   # Sets minimum and maximum attenuation for all channels
   min,10
   max,900
   # Directives: MINIMUM,MAXIMUM,MIN,MAX,minimum,min,maximum and max are allowed

   #  The next line defines column B as attenuator channel 1.1.13.1
   #  and column C as attenuator channel 2.1.25.1. Remember that
   #  attennuator channels are values (shelf).(resource).(serialno).(channel)
   #  and channels are presently values {1, 2, 3, 4}.
   channels,1.1.13.1,2.1.25.1
   # Directives: CHANNELS,channels are equivalent

   # Attenuation values are in deci-dBm, resolution of 5ddB:
   # The next line sets 1.1.13.1 to 36.5dB, 2.1.25.1 to 30.0dB:
   attenuate,365,300
   # Directives: ATTENUATE,attenuate, "", and _ are equivalent.
   
   # The next line leaves 1.1.13.1 alone, sets 2.1.25.1 to 31.0dB,
   # _ is an abbreviation for attenuate
   _,NA,+10
   # The next line leaves 1.1.13.1 alone, sets 2.1.25.1 to 30.5dB,
   # Blank first column is an abbreviation for attenuate
   ,NA,-5
   
   # Only some basic CSV formulas are interpretable, and only operate
   # on the previous values of the attenuator; the next line sets
   # sets 1.1.13.1 to 36.0dB, sets 2.1.25.1 to 31.0dB
   ,=B6-5,=C6+5
   
   # does nothing for a period
   _,_,NA,,
   
   # does nothing for 35ms
   sleep,35
   # Directives: SLEEP,sleep, and nap are equivalent
);


our $csvfile         = undef;
our $delay           = -1;
our $delay_override  = -1;
our $do_loop         = 0;
our @channels        = (); # in order list of channels
our %last_atten      = (); # a map of last-known values
our $channel_override= undef;
our $quiet           = "yes";
our $line            = 0; # line number
our $lfmgr_host      = "localhost";
our $lfmgr_port      = 4001;
our $dryrun          = 0;
our $min_atten       = 0;
our $max_atten       = 995;

GetOptions (
   'manager|mgr|m=s'    => \$::lfmgr_host,
   'mgr_port|port|p=i'  => \$::lfmgr_port,
   'file|f=s'           => \$::csvfile,
   'delay|d=i'          => \$::delay_override,
   'loop|l'             => \$::do_loop,
   'channels|c'         => \$::channel_override,
   'quiet|q=s'          => \$::quiet,
   'dry_run|dry|n'      => \$::dryrun,
   'minimum|min|mn|i=i' => \$::min_atten,
   'maximum|max|mx|x=i' => \$::max_atten,
) || die("$::usage");

die("Please specify a manager address;\n$::usage") 
   if (!defined $::lfmgr_host || "$::lfmgr_host" eq "");

die("Please specify a csv file;\n$::usage")
   if (!defined $::csvfile || "$::csvfile" eq "");

die("Unable to find csv file: $::csvfile")
   unless(-f $::csvfile );

our $cfile=new LANforge::csv();
$::cfile->readFile($::csvfile);

if ($::cfile->numRows < 1) {
   die( "empty file, nothing to do");
}

if ($::quiet eq "1" ) {
   $::quiet = "yes";
}
elsif ($::quiet eq "0" ) {
   $::quiet = "no";
}

if (defined $::channel_override && "$::channel_override" != "") {
   for my $c ( split(/,/, $::channel_override)) {
      push(@::channels, $c);
      $::last_atten{$c} = 0;
   }
}

die("Minimum attenuation must be between [0-954]")
   if ($::min_atten > 994 || $::min_atten < 0);
die("Maximum attenuation must be between [1-995]")
   if ($::max_atten > 995 || $::max_atten < 1);
die("Minimum attenuation must be less than maximum attenuation")
   if ($::max_atten <= $::min_atten);

sub lastAtten {
   my $arg = shift;
   die ("lastAtten: called without argument") 
      if (! defined $arg || "$arg" eq "");
   if ($arg =~ /^\d+$/) {
      if (!defined($::channels[$arg])) {
         warn "Channels: ".join(', ', @::channels);
         die ("no channel recorded at position $arg");
      }
      die ("no channel [$::channels[$arg]]")
         if (!defined $::last_atten{$::channels[$arg]});

      return $::last_atten{$::channels[$arg]};
   }
   elsif ($arg =~ /^\d+\.\d+\.\d+\.\d+$/) {
      die ("no channel [$::channels[$arg]]")
         if (!defined $::last_atten{$::channels[$arg]});

      return $::last_atten{$arg};
   }
   die ("lastAtten: What is channel $arg?");
}

sub attenuate {
   my $channel = shift;
   my $value   = shift;

   die("attenuate: no line number") 
      if (!defined $::line || "$::line" eq "");
   die("attenuate: $::line: no channel") 
      if (!defined $channel || "$channel" eq "");

   return if (!defined $value || "$value" eq "");
   return if (lc($value) =~ /^(na|_)$/);
   return if (lc($value) =~ /^\s*[!;\#]/);

   my ($shelf, $resource, $serno, $chan) = split(/\./, $channel);
   #print "shelf:$shelf, r:$resource, ser:$serno, ch:$chan\n";
   die( "[$::line] attenuate: shelf misconfigured:[$channel][$value]")
      if ($shelf != 1);

   die( "[$::line] attenuate: resource misconfigured:[$channel][$value]")
      if ($resource < 1);

   die( "[$::line] attenuate: serial number misconfigured:[$channel][$value]")
      if ($serno < 1);

   die( "[$::line] attenuate: channel misconfigured:[$channel][$value]")
      if ($chan < 0 || $chan > 4);
  
   my $prev_value = $::last_atten{$channel};
   if ($value =~ /^[-+]/) {
      die("[$::line] attenuate: no previous value set for $channel")
         if (! defined $prev_value);

      $value = $prev_value + (0+$value);
      #warn "VALUE MATH[$value] ";
   }

   if ($value > $::max_atten)  {
      warn("[$::line] attenuate: value cannot be higher than $::max_atten")
         unless($::quiet eq "yes");
      $value = $::max_atten;
   }

   if ($value < $::min_atten) {
      warn("[$::line] attenuate: value cannot be lower than $::min_atten")
         unless($::quiet eq "yes");
      $value = $::min_atten;
   }

   $::last_atten{$channel} = $value;
   $::utils->doAsyncCmd("set_atten $shelf $resource $serno $chan $value")
      unless (defined $::dryrun && $::dryrun);

   print "$::line: set_atten $shelf.$resource.$serno.$chan $value\n"
      if ($::quiet ne "yes" || $::dryrun);
}
##
##    M A I N
##

# connect to manager
our $utils = new LANforge::Utils();
$utils->connect($lfmgr_host, $lfmgr_port);
if ($::quiet eq "yes") {
  $::utils->cli_send_silent(1); # Do show input to CLI
  $::utils->cli_rcv_silent(1);  # Repress output from CLI ??
}
else {
  $::utils->cli_send_silent(0); # Do show input to CLI
  $::utils->cli_rcv_silent(0);  # Repress output from CLI ??
}


if (defined $::delay_override && $::delay_override != -1 && $::delay_override < 1000) {
   warn("$0: --delay is in milliseconds, values less than 1000 (1 second) might be meaningless");
   sleep 2;
}
die ("$0: --delay of zero or less is not permitted.")
   if (defined $::delay_override && $::delay_override != -1 && $::delay_override <= 0);

$::delay = $::delay_override if (defined $::delay_override && $::delay_override > 0);

my $loop_count = 0;
while ($loop_count == 0 || $::do_loop) {
   $loop_count++;
   for (my $rownum = 0; $rownum < $::cfile->numRows(); $rownum++) {
      $::line     = $rownum+1;
      my $ra_row  = $::cfile->getRow($rownum);
      
      next if (@{$ra_row} == 0); # empty row

      if (lc($ra_row->[0]) =~ /^(delay|naptime)$/) {
         next if (defined $::delay_override && $::delay_override != -1);

         $::delay = 0 + $ra_row->[1];
         die ("$line: delay of zero or less is not permitted")
            if ($::delay <= 0);
         next;
      }

      if (lc($ra_row->[0]) =~  /^channels$/ && (!defined $::channel_override)) {
         my @tempchannels = @$ra_row;
         shift @tempchannels;
         %::last_atten= ();
         for my $c (@tempchannels) {
            push(@::channels, $c);
            $::last_atten{$c} = -1;
         }
         next;
      }

      if (lc($ra_row->[0]) =~ /^(sleep|nap)$/) {
         if (!defined $ra_row->[1] || (0 + $ra_row->[1]) < 1) {
            die("$line: sleep value needs to be 1ms or greater");
         }
         usleep($ra_row->[1] *1000) unless ($::dryrun);
         next;
      }

      if (lc($ra_row->[0]) =~ /^(attenuate|_)$/ || $ra_row->[0] eq "") {
         #print "\n";
         my $col        = 1;
         foreach my $ch (@::channels) {
            my $value   = "NA";
            my $data    = $::cfile->getCell($col, $rownum, "na");
            #print "DATA($col,$::line)[$data] ";

            if (!defined $data || "$data" eq "" ) { 
               $col++;
               next;
            }
            if (lc($data) =~ /^(na|_)$/ || $data =~ /^\s*\#.*$/) {
               #warn ("skipping data[$data] at $col,$::line");
               $col++;
               next;
            }
            if ($data =~ /^\d+$/) {
               $value   = 0 + $data;
            }
            elsif ($data =~ /^=[B-Z]\d+[+-]\d+$/i) { # we have a formula
               my ($acol,$arow,$delta) = $data =~ /^=([B-Z])(\d+)([+-]\d+)$/i;
               $acol    = ord(uc($acol)) - 65;
               my $pval = $::cfile->getCell($acol, $arow-1, 0);
               if (!defined $pval) {
                  $pval = lastAtten($col-1);# $::last_atten{$::channels[$col]};
                  warn("Failed to find valid references at cell[$col,$::line], using previous attenuation:".$pval);
               }
               if ( $pval !~ /^\d+$/) {
                  $value = lastAtten($col-1);# $::last_atten{$::channels[$col]};
                  die("Failed to find valid references at cell[$col,$::line]:".$value)
                     if ( ! defined $value);

                  #$value = $value + (0+$delta);
                  warn "Substituting [$value]: cell[$col,$::line] refers to cell[$acol,$arow] with non absolute value:$pval";
               }
               else {
                  $value   = $pval + (0 + $delta);
               }
               #print "acol[$acol] arow[$arow] delta[$delta] pval[$pval] value[$value]\n";
            }
            elsif ($data =~ /^\@?[+]+\d+$/ ) { # add relative
               my ($delta) = $data =~ /^\@?[+]+(\d+)$/;
               my $pval    = lastAtten($col-1); #$::last_atten{$::channels[$col]};
               $value      = $pval + (0 + $delta);
            }
            elsif ( $data =~ /^\@?[-]+\d+$/ ) { # subtract relative
               my ($delta) = $data =~ /^\@?[-]+(\d+)$/;
               my $pval    = lastAtten($col-1); #$::last_atten{$::channels[$col]};
               $value      = $pval + (-1 * (0 + $delta));
            }
            else {
               warn "Unknown directive[$data] ";
               $col++;
               next;
            }
            attenuate($ch, "$value");
            $col++;
         }

         die("Step delay not set correctly[$::delay]") 
            if (!defined $::delay || "$::delay" eq "" || (0+$::delay) < 1);

         usleep($::delay * 1000) unless ($::dryrun);
         next
      }
      die("$::line: unknown directive[".$ra_row->[0]);
   }
}

## eof
