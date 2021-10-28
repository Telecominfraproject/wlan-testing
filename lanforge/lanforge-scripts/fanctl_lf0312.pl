#!/usr/bin/perl -w
use strict;
use warnings;
use diagnostics;

$|=1;
package main;
our $fan_util = "/usr/local/bin/f81866_fan";
if ( ! -x $fan_util ) {
   die "f81866_fan utility $fan_util not found\n";
}

my @sensor_lines_a = `sensors`;
chomp(@sensor_lines_a);
my @sensor_lines_b = grep ! /^\s*$/, @sensor_lines_a;
@sensor_lines_a = grep ! /^(Physical id|Core|coretemp|Adapter: ISA adapter)/, @sensor_lines_b;

#print ("Found: ".join("\n", @sensor_lines_a));
my $found_a10k = 0;
my $temp       = 0;
my $maxtemp    = 0;
for my $line (@sensor_lines_a) {
   if ($line =~ /^ath10k_hwmon-pci.*/) {
      #print "found a10k! $line\n";
      $found_a10k = 1;
   }
   if ($found_a10k && $line =~ /temp1:\s+([^ ]+).*$/) {
      #print "found a10k: $line\n";
      if ($1 ne "N/A") {
         ($temp) = $line =~ /[+](\d+\.\d+)/;
         if (defined $temp && $temp > 40.0) {
            $maxtemp = $temp if ($temp > $maxtemp);
            #print "temp($temp) maxtemp($maxtemp)\n";
         }
         $temp = 0;
      }
      $found_a10k = 0;
   }
}

my $duty = 0;
if ($maxtemp < 40) {
   $duty = 0;
}
elsif ($maxtemp < 50) {
   $duty = 50;
}
elsif ($maxtemp < 56) {
   $duty = 55;
}
elsif ($maxtemp < 60) {
   $duty = 60;
}
elsif ($maxtemp < 70) {
   $duty = 70;
}
elsif ($maxtemp < 80) {
   $duty = 80;
}
elsif ($maxtemp >= 80) {
   $duty = 100;
}

#print "[$maxtemp]C -> duty[$duty]\n";
system("/usr/bin/logger -t fanctl_lf0312 'temp:$maxtemp C, duty:$duty'");
exec("$fan_util $duty");

#
