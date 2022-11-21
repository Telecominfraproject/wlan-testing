#!/usr/bin/perl -w
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
# This script looks for min-max-average bps for rx_rate in 
# a station csv data file
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
package main;
$| = 1; # unbuffer output
use strict;
use warnings;
use diagnostics;
use Carp;
use Getopt::Long;
use POSIX qw(locale_h);
use locale;
use Number::Format qw(format_number);

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
our $TimeStamp       = 0;
our $Name            = 1;
our $Resource        = 3;
our $Tx_Pkts         = 4;
our $Tx_Packets      = 4;
our $Rx_Pkts         = 5;
our $Rx_Packets      = 5;
our $Tx_Bytes        = 6;
our $Rx_Bytes        = 7;
our $Rx_Signal       = 25;
our $Link_Speed      = 26;
our $Rx_Link_Speed   = 27;

our $filename;
our $start_time      = 0;
our $finish_time     = time() * 1000;

our $usage = "$0 [-f|--filename      # name of staX csv file]
            [-s|--start_time        # timestamp milliseconds point to begin]
            [-e|--finish_time       # timestamp milliseconds point to finish]

Example:
$0 -f ./sta100_1.1.5_1429826436.csv # collect all entries

$0 -s 1429820000 -e 1429828000 -f ./sta100_1.1.5_1429826436.csv

We can use expanded unix datestamps as well:
$0 -s \`date -d \"2014/11/25 10:00:00\" \"+%s000\"\` \\
   -e \`date -d \"2014/11/25 11:00:00\" \"+%s000\"\` \\
   -f ./sta100_1.1.5_1429826436.csv
";

sub do_err_exit {
  my $msg = shift;
  print $msg."\n";
  exit(1);
}

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
# takes a reference to a string
sub printRow {
   my $rs_line  = shift;
   #print "LINE: $$rs_line\n";
   my @hunks   = split(',', $$rs_line);
   my $msg     = 
"TimeStamp       : $hunks[$::TimeStamp]
Name            : $hunks[$::Name]
Resource        : $hunks[$::Resource]
Tx_Pkts         : $hunks[$::Tx_Pkts]
Rx_Pkts         : $hunks[$::Rx_Pkts]
Tx_Bytes        : $hunks[$::Tx_Bytes]
Rx_Bytes        : $hunks[$::Rx_Bytes]
Rx_Signal       : $hunks[$::Rx_Signal]
Link_Speed      : $hunks[$::Link_Speed]
Rx_Link_Speed   : $hunks[$::Rx_Link_Speed]\n\n";

   print $msg;
}
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
# takes a reference to an array
 sub printRowAt {
   my $ra_rows    = shift;
   my $index      = shift;
   my $row        = $ra_rows->[$index];
   printRow( \$row );
}
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
#     M A I N                                                       #
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
GetOptions (
   'filename|f=s'         => \$::filename,
   'start_time|s=i'       => \$::start_time,
   'finish_time|e=i'      => \$::finish_time
) || do_err_exit("$usage");

if ( ! defined $::filename || $::filename eq "" ) {
   do_err_exit($::usage);
}
if ( ! -f $::filename ) {
   do_err_exit("file not found");
}
open (my $input_fh, "<", $::filename) || do_err_exit($!);
my @lines = <$input_fh>;
close($input_fh);

#my $first_line = $lines[0];
#printRow( \$first_line );
#printRowAt( \@lines, 0 );

our $Orig   = 0;
our $Min    = 1;
our $Max    = 2;
our $Tot    = 3;
our $Total  = 3;
our $Ave    = 4;
our $Avg    = 4;
our $Delta  = 5;
our $Dt     = 5;

my @begin_rx_bytes;
my @begin_rx_packets;
my @begin_rx_signal;
my $begin_time = 0;

my @cur_rx_bytes;
my @cur_rx_packets;
my @cur_rx_signal;

my @prev_rx_bytes;
my @prev_rx_packets;
my @prev_rx_signal;

# first entry
#my @hunks = split(',', $lines[ 1 ]);
my $counted = 0;
for( my $i = 2 ; $i < $#lines ; $i++ ) {
   my @hunks = split(',', $lines[$i]);

   #print "start time: $::start_time\nfinish time: $::finish_time\ntime stamp : $hunks[$::TimeStamp]\n";
   next if ($hunks[ $::TimeStamp ] < $::start_time );
   last if ($hunks[ $::TimeStamp ] > $::finish_time );

   if ($counted == 0) {
      $begin_time                  = $hunks[$::TimeStamp];
      $begin_rx_bytes[   $::Orig ] = $hunks[$::Rx_Bytes];
      $begin_rx_bytes[    $::Min ] = $hunks[$::Rx_Bytes];
      $begin_rx_bytes[    $::Max ] = $hunks[$::Rx_Bytes];
      $begin_rx_bytes[    $::Tot ] = $hunks[$::Rx_Bytes];
      $begin_rx_bytes[    $::Ave ] = $hunks[$::Rx_Bytes];
      $begin_rx_bytes[  $::Delta ] = 0;

      $begin_rx_packets[ $::Orig ] = $hunks[$::Rx_Packets];
      $begin_rx_packets[  $::Min ] = $hunks[$::Rx_Packets];
      $begin_rx_packets[  $::Max ] = $hunks[$::Rx_Packets];
      $begin_rx_packets[  $::Tot ] = $hunks[$::Rx_Packets];
      $begin_rx_packets[$::Delta ] = 0;

      $begin_rx_signal[ $::Orig ] = $hunks[$::Rx_Signal];
      $begin_rx_signal[  $::Min ] = $hunks[$::Rx_Signal];
      $begin_rx_signal[  $::Max ] = $hunks[$::Rx_Signal];
      $begin_rx_signal[  $::Tot ] = $hunks[$::Rx_Signal];
      $begin_rx_signal[$::Delta ] = 0;
      @cur_rx_bytes     = @begin_rx_bytes;
      @cur_rx_packets   = @begin_rx_packets;
      @cur_rx_signal    = @begin_rx_signal;
   }
   @prev_rx_bytes       = @cur_rx_bytes;
   @prev_rx_packets     = @cur_rx_packets;
   @prev_rx_signal      = @cur_rx_signal;

   #printRowAt( \@lines, $i );

   $cur_rx_bytes[ $::Orig ] = $hunks[ $::Rx_Bytes ];
   my $diff_rx = $hunks[ $::Rx_Bytes ] - $prev_rx_bytes[ $::Orig ];
   $cur_rx_bytes[ $::Delta ] = $diff_rx;

   if ($hunks[$::Rx_Bytes]==0) {
      print "TimeStamp $hunks[$::TimeStamp] zero bytes\n";
      $cur_rx_bytes[ $::Min ] = 0;
   }
   elsif (($diff_rx < $prev_rx_bytes[ $::Delta ]) && ($diff_rx < $prev_rx_bytes[ $::Min ])) {
      if ($diff_rx == 0) {
         print "TimeStamp $hunks[$::TimeStamp] zero bytes diff\n";
         $cur_rx_bytes[ $::Min ] = $prev_rx_bytes[ $::Delta ];
      } else {
         $cur_rx_bytes[ $::Min ] = $diff_rx;
      }
   }
   if (($diff_rx > $prev_rx_bytes[ $::Delta ]) && ($diff_rx > $prev_rx_bytes[ $::Max ])) {
      $cur_rx_bytes[ $::Max ] = $diff_rx;
   }
   $cur_rx_bytes[    $::Tot ] = $hunks[ $::Rx_Bytes ] - $begin_rx_bytes[ $::Orig];

   

   $cur_rx_packets[ $::Orig ] = $hunks[ $::Rx_Packets ];
   $diff_rx = $hunks[ $::Rx_Packets ] - $prev_rx_packets[ $::Orig ];
   $cur_rx_packets[ $::Delta ] = $diff_rx;

   if ($hunks[$::Rx_Packets]==0) {
      print "TimeStamp $hunks[$::TimeStamp] zero packets\n";
      $cur_rx_packets[ $::Min ] = 0;
   }
   elsif (($diff_rx < $prev_rx_packets[ $::Delta ]) && ($diff_rx < $prev_rx_packets[ $::Min ])) {
      if ($diff_rx == 0) {
         print "TimeStamp $hunks[$::TimeStamp] zero packets diff\n";
         $cur_rx_packets[ $::Min ] = $prev_rx_packets[ $::Delta ];
      } else {
         $cur_rx_packets[ $::Min ] = $diff_rx;
      }
   }
   if (($diff_rx > $prev_rx_packets[ $::Delta ]) && ($diff_rx > $prev_rx_packets[ $::Max ])) {
      $cur_rx_packets[ $::Max ] = $diff_rx;
   }
   $cur_rx_packets[  $::Tot ] = $hunks[ $::Rx_Packets ] - $begin_rx_packets[ $::Orig ];


   $cur_rx_signal[ $::Orig ]  = $hunks[ $::Rx_Signal ];
   $cur_rx_signal[  $::Min ]  = $hunks[ $::Rx_Signal ] if ( $hunks[ $::Rx_Signal ] < $prev_rx_signal[ $::Min ]);
   $cur_rx_signal[  $::Max ]  = $hunks[ $::Rx_Signal ] if ( $hunks[ $::Rx_Signal ] > $prev_rx_signal[ $::Max ]);
   $cur_rx_signal[  $::Tot ]  = $prev_rx_signal[ $::Tot ] + $hunks[ $::Rx_Signal ];

   $counted++;
}
my $seconds = ($finish_time - $begin_time + 1000) / 1000;

if ($seconds <= 0 || $counted <= 0) {
   do_err_exit("No records in range");
}
$cur_rx_bytes[ $Ave ]   =  $cur_rx_bytes[ $::Tot ]   / $counted;
$cur_rx_packets[ $Ave ] =  $cur_rx_packets[ $::Tot ] / $counted;
$cur_rx_signal[ $Ave ]  =  $cur_rx_signal[ $::Tot ]  / $counted;

printf "Rx Bytes:   Min_Bps: %15s  Max_Bps: %15s  Ave_Bps: %15s  Total: %15s\n",
      format_number($cur_rx_bytes[ $::Min ]),
      format_number($cur_rx_bytes[ $::Max ]),
      format_number($cur_rx_bytes[ $Ave ]),
      format_number($cur_rx_bytes[ $::Tot ]);

printf "Rx bits/sec Min_bps: %15s  Max_bps: %15s  Ave_bps: %15s\n",
      format_number($cur_rx_bytes[ $::Min ] * 8),
      format_number($cur_rx_bytes[ $::Max ] * 8),
      format_number($cur_rx_bytes[ $Ave ]   * 8);

printf "Rx Packets: Min_Pps: %15s  Max_Pps: %15s  Ave_Pps: %15s  Total: %15s\n",
      format_number($cur_rx_packets[ $::Min ]),
      format_number($cur_rx_packets[ $::Max ]),
      format_number($cur_rx_packets[ $Ave ]),
      format_number($cur_rx_packets[ $::Tot ]);

printf "Rx Signal:  Min_dB:  %15s  Max_dB: %16s  Ave_dB:  %15s\n",
      format_number($cur_rx_signal[ $::Min ]),
      format_number($cur_rx_signal[ $::Max ]),
      format_number($cur_rx_signal[  $Ave ]);
print format_number($counted)." samples in ".format_number($seconds)." seconds\n";
##
##
##
