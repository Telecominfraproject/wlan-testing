#!/usr/bin/perl

# Convert LANforge logs and hostapd log timestamps to human readable timestamp.

use POSIX qw( strftime );

while (<>) {
  my $ln = $_;
  if ($ln =~ /^(\d+)\.(\d+): (.*)/) {
    my $time_sec = $1;
    my $usec = $2;
    my $rest = $3;
    my $usec_pad = sprintf("%06d", $usec);
    my $dt = strftime("%Y-%m-%d %H:%M:%S", localtime($time_sec));
    print "$dt.$usec_pad $rest\n";
  }
  elsif ($ln =~ /^(\d+): (.*)/) {
    my $tot_msec = $1;
    my $rest = $2;
    my $sec = int($tot_msec / 1000);
    my $msec = $tot_msec % 1000;
    my $msec_pad = sprintf("%03d", $msec);
    my $dt = strftime("%Y-%m-%d %H:%M:%S", localtime($sec));
    print "$dt.$msec_pad $rest\n";
  }
  else {
    print $ln;
  }
}
