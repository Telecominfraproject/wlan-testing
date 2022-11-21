#!/usr/bin/perl
#
use strict;
use warnings;
use diagnostics;
use Carp;
$SIG{__DIE__} = sub{Carp::confess(@_)};
use Getopt::Long;
use Time::HiRes qw(usleep);
use List::Util qw(sum min max);

$| = 1;
package main;
our @file_lines;
our $success_counter    = 0;
our $fail_counter       = 0;
our %station_names      = ();
our @association_times  = ();
die "Want a wpa_supplicant_log.wiphyX file please, bye.\n"
   unless(defined $ARGV[0]);

die "I can't find $ARGV[0], sorry."
   unless(-f $ARGV[0]);

die $!
   unless open(my $fh, "<", $ARGV[0]);
@file_lines = <$fh>;
close $fh;
chomp(@file_lines);

# survey for all the station names
#
for (@file_lines) {
   next unless /: (sta\d+): /;
   $station_names{ $1 } = 0
      unless(defined $station_names{ $1 } );
}
print "Found these stations: ";
while( my($k, $v)= each %station_names) {
   print "$k, ";
}
print "\n";

# for each station, find the BSS of the thing it's attempting to roam for
while( my($sta, $v)= each %station_names) {
   my @lines_by_station    = grep {/: $sta: /} @file_lines;
   #print "lines for $sta: ".@lines_by_station."\n";
   my $is_roam_attempt     = 0;
   my $target_bss          = "";
   my $prev_bss            = "";
   my $time_roam_start     = 0;
   my $time_roam_stop      = 0;
   my $time_roam_delta     = 0;
   my @roam_lines = ();
   usleep(50000);
   for (@lines_by_station) {
      #print "$sta : $is_roam_attempt, $target_bss, $prev_bss, $fail_counter, $success_counter\n";
      if (/ SME: Trying to authenticate with ([^ ]+) /) {
         if ($is_roam_attempt == 1) {
            $fail_counter ++ ;
            $prev_bss = $target_bss;
         }
         
         #print "$sta trying bss $1\n";
            
         $is_roam_attempt = 1;
         $target_bss = $1;
         ($time_roam_start) = /^(\d+\.\d+): /;
         next;
      }
      push(@roam_lines, $_);
      # else  we're in the middle of a roaming attemt
      if (/: CTRL-EVENT-CONNECTED - Connection to ([0-9A-Fa-f:]+) completed/) {
         #print "connected bss $1\n";
         die "aaaa!"
            if ($target_bss eq "");
         if ($prev_bss eq $1) {
            #print "Roam to self? $prev_bss\n";
            #print join("\n", @roam_lines)."\n";
         }

         $is_roam_attempt = 0;
         if ($target_bss eq $1) {
            $success_counter ++ ;
            $prev_bss = $target_bss;
         }
         
         ($time_roam_stop) = $_ =~ /^(\d+\.\d+): /;
         $time_roam_delta = $time_roam_stop - $time_roam_start;
         die ("What an unlikely roam time you have my dear: $time_roam_delta")
            if ($time_roam_delta <= 0);

         #print "$sta roam to $target_bss in $time_roam_delta\n";
         push(@association_times, $time_roam_delta);
         @roam_lines = ();
         $time_roam_start = 0;
         $time_roam_stop  = 0;
         $time_roam_delta = 0;
      }
      #usleep(5000);

   } # ~for

   #my $ave = sum(@association_times)/@association_times
   #   unless (@association_times < 1);
   #
   # print "$sta +$success_counter -$fail_counter > $ave\n"

} # ~while

my $ave = sum(@association_times)/@association_times
   unless (@association_times < 1);
my $min = min(@association_times);
my $max = max(@association_times);

my $i = 0;
for (sort {$a <=> $b}  @association_times) {
   print "$_ " if ($i <= 9); 
   print "$_ " if ($i >= @association_times -9); 
   $i++;
}
print "\n";

print "Roam Successes: $success_counter\n";
print "Roam Failures:  $fail_counter\n";
print "Min/Ave/Max:    $min $ave $max\n";


# find CTRL-EVENT-CONNECTED and if we connect to that BSS we're good
# compute a time factor, and record it

