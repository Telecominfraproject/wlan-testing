#!/usr/bin/perl -w
#
# Log the traffic generating processing processes that LANforge creates
# This script will increase system logging usage (journalctl via logger)
# so if you need to add runtime constraints for disk usage, please add these
# runtime settings to you /etc/systemd/journald.conf file:
#   SystemMaxUse=100M
#   RuntimeMaxUse=1024M
#   RuntimeKeepFree=500M
#   RuntimeMaxFiles=5
#   RuntimeMaxFileSize=256M
#
# Follow these message through journalctl using this technique:
#
#   sudo ./loadmon.pl | logger -t loadmon
# ...new terminal...
#   watch -n15 'journalctl --since "20 sec ago" -t loadmon | ./parse_loadmon.pl'
#

use diagnostics;
use warnings;
use strict;
#use Time::localtime;
use POSIX;
use Data::Dumper;
$| = 1;

package main;

our $QQ=q{"};
our $Q=q{'};
our $LC=q({);
our $RC=q(});

our @prog_names = (
    "btserver",
    "curl",
    "dhclient",
    "dnsmasq",
    "hostapd",
    "httpd",
    "iw",
    "java",
    "l4helper",
    # "logchopper",
    "nginx",
    "perl",
    "php-fpm",
    "pipe_helper",
    "vsftpd",
    "wget",
    "wpa_cli",
    "wpa_supplicant",
);
our %monitor_map = ();

## - - - Define loadmon - - - ##
package loadmon;
sub new {
    my $class = shift;
    my ( $basename ) = @_;
    my $self = {
        basename => $basename,
        ra_pid_list => [],
        total_mem => 0,
        total_fh => 0,
        total_thr => 0,
    };
    bless $self, $class;
    return $self;
}

sub monitor {
    my $self = shift;
    $self->{total_mem} = 0;
    $self->{total_fh} = 0;
    $self->{total_threads} = 0;

    my $cmd = qq(pgrep -f $self->{basename});
    # print "CMD[$cmd]\n";
    my @lines = `$cmd`;
    chomp(@lines);
    # print Data::Dumper->Dump(\@lines);
    $self->{ra_pid_list} = [];
    splice @{$self->{ra_pid_list}}, 0, 0, @lines;
    if ( scalar( @{$self->{ra_pid_list}} ) < 1) {
        return;
    }
    # print Data::Dumper->Dump(['ra_pid_list', $self->{ra_pid_list}] ), "\n";
    my $pidlist = join(" ", @{$self->{ra_pid_list}});
    $cmd = qq(echo $pidlist | xargs ps -o rss -p | tail -n+2);
    # print "CMD2: $cmd\n";
    my @mem_lines=`$cmd`;
    chomp(@mem_lines);
    #print Data::Dumper->Dump(['mem_lines', \@mem_lines]), "\n";
    for my $mem (@mem_lines) {
        $self->{total_mem} += int($mem);
    }

    for my $pid (@{$self->{ra_pid_list}}) {
        next unless ( -d "/proc/$pid/fd" );
        $cmd = "ls /proc/$pid/fd | wc -l";
        @lines=`$cmd`;
        chomp(@lines);
        # print Data::Dumper->Dump(['fh_lines', \@lines]), "\n";
        if (@lines > 0 ) {
            $self->{total_fh} += int($lines[0]);
        }
        $cmd = "ls /proc/$pid/task/ | wc -l";
        my $threads = `$cmd`;
        chomp $threads;
        $self->{total_threads} += int($threads);
    }

    #die("testing");
}

sub report {
    my ($self, $fh) = @_;
    my $num_pids = 0 + @{$self->{ra_pid_list}};

    # print Data::Dumper->Dump(['report', $self] ), "\n";
    if ($num_pids < 1) {
        print $fh "0";
        return;
    }
    if (!$fh) {
        $fh = *STDOUT;
    }
    print $fh qq(${LC}"basename":"$self->{basename}",);
    print $fh qq("num_pids":$num_pids,);
    print $fh qq("total_mem_KB":$self->{total_mem},);
    print $fh qq("total_fh":$self->{total_fh},);
    print $fh qq("total_threads":$self->{total_threads}${RC});
}
1;
## - - - End loadmon - - - ##

## - - - Define main - - - ##
package main;

sub print_totals {
    my $fh = shift;
    if (!$fh) {
        $fh = *STDOUT;
    }
    my $tt_num_pids = 0;
    my $tt_mem_kb = 0;
    my $tt_fh = 0;
    my $tt_threads = 0;
    for my $name (@main::prog_names) {
        my $monitor = $main::monitor_map{$name};
        #print Data::Dumper->Dump(["mm_name", $monitor ]);
        my $ra_pl = $monitor->{ra_pid_list};
        #print Data::Dumper->Dump(["ra_pl", $ra_pl]);
        $tt_num_pids += @$ra_pl;
        if (defined $main::monitor_map{$name}->{total_mem}) {
            $tt_mem_kb += $main::monitor_map{$name}->{total_mem};
        }
        $tt_fh += $main::monitor_map{$name}->{total_fh};
        $tt_threads += $main::monitor_map{$name}->{total_threads};
    }
    print $fh qq(${LC}"tt_num_pids":$tt_num_pids, "tt_mem_kb":$tt_mem_kb, "tt_fh":$tt_fh, "tt_threads":$tt_threads${RC});
}

## - - -
#           M A I N
## - - -
for my $name (@main::prog_names) {
    $monitor_map{$name} = loadmon->new($name);
}


while (1) {
    print STDOUT '[';
    for my $name (@main::prog_names) {
        my $lmonitor = $monitor_map{$name};
        # print "$name ";
        $lmonitor->monitor();
        $lmonitor->report(*STDOUT);
        print ",";
    }
    print_totals(*STDOUT);
    print "]\n";
    sleep(5);
}
#
