#!/usr/bin/perl -w

# Follow these message through journalctl using this technique:
#
#   Read from a pipe or a fifo:
#       sudo ./loadmon | ./parse_loadmon.pl
#
#       mkfifo /tmp/load.fifo
#       ./parse_loadmon.pl < /tmp/load.fifo
#       sudo ./loadmon > /tmp/load.fifo
#
#   Loadmon output is now longer than journalctl line limits, so the
#   below example will not work:
#   sudo ./loadmon.pl | logger -t loadmon
# ...new terminal...
#   watch -n15 'journalctl --since "20 sec ago" -t loadmon | ./parse_loadmon.pl'

#

use strict;
use warnings;
use diagnostics;
use JSON::Parse qw(parse_json);
use Data::Dumper;

$| = 1;

sub mb {
    my $kb = shift;
    if ($kb < 1024) {
        return "${kb}KB";
    }
    my $mb = $kb / 1024;
    return sprintf("%0.1f MB", $mb);
}

while (my $line=<STDIN>) {
    chomp $line;
    # print "line[$line]\n";
    my $lc_pos = index($line, '[{');
    # print "lc at $lc_pos\n";
    next if ($lc_pos < 0);
    print `date`;
    my $loadmon_line = substr($line, $lc_pos);
    my $ra_loadmon = parse_json($loadmon_line);
    #print Dumper($ra_loadmon);

    for my $rh_item ( @$ra_loadmon) {
        next if ($rh_item == 0);
        if (defined($rh_item->{basename})) {
            printf("%-15s: %3d pids (%4d thr) use %9s memory\n",
                    $rh_item->{basename},
                    $rh_item->{num_pids},
                    $rh_item->{total_threads},
                    mb($rh_item->{total_mem_KB}));
        }
        else {
            printf("TOTALS : %11d pids (%4d thr) use %9s ram and %7d FH\n\n",
                    $rh_item->{tt_num_pids},
                    $rh_item->{tt_threads},
                    mb($rh_item->{tt_mem_kb}),
                    $rh_item->{tt_fh});
        }
    }
}
