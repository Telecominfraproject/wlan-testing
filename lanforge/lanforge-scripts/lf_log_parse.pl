#!/usr/bin/perl

# Convert the timestamp in LANforge logs (it is in unix-time, miliseconds)
# to readable date.

use strict;
use POSIX qw(strftime);

while (<>) {
  my $ln = $_;
  chomp($ln);
  if ($ln =~ /^(\d+):(.*)/) {
    my $ts = $1;
    my $rst = $2;
    my $dt = strftime("%Y-%m-%d %H:%M:%S", localtime($ts / 1000));
    my $msec = $ts % 1000;
    print "$dt $msec:$rst\n";
  }
  else {
    print "$ln\n";
  }
}
