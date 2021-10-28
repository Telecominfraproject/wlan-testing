#!/usr/bin/perl -w
package main;
use strict;
use warnings;
use feature qw(switch);
use Data::Dumper;
use Carp;
$SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
$SIG{ __WARN__ } = sub { Carp::confess( @_ ) };
#use File::IO;
use Getopt::Long;
use File::Copy qw(cp);
use File::Temp qw(tempfile tempdir);
use POSIX qw(strftime ceil floor abs);
#use MIME::Base64 qw();
use Cwd;
$| = 1;

=pod
################################################################################
#                                                                              #
#  Use this script to reconfigure apache Listen directives so that it only     #
#  listens on ports 127.0.0.1:80 and mgt_dev:80. This is to allow lanforge     #
#  versions of nginx to listen on managed ports without conflict. Run this     #
#  script every time you run /home/lanforge/lfconfig.                          #
#                                                                              #
################################################################################
=cut

our $is_fedora=0;
our $is_centos=0;
our $is_ubuntu=0;

sub error {
   for (@_) {
      print STDERR "$_\n";
   }
}

if (!-f "/etc/os-release") {
   die("no /etc/os-release, bye.");
}
my @os_release_lines = `cat /etc/os-release`;
my @os_name_lines = grep {/^NAME=/} @os_release_lines;
die ("Unknown OS") if (@os_name_lines < 1);

if ($os_name_lines[0] =~ /CentOS( Linux)?/) {
   $is_centos = 1;
}
elsif ($os_name_lines[0] =~ /\bFedora\b/) {
   $is_fedora = 1;
}
elsif ( $os_name_lines[0] =~ /\bUbuntu\b/) {
   $is_ubuntu = 1;
}
else {
   die("Unknown OS: $os_name_lines[0]");
}

my @new_httpconf_lines = ();
if ((! -d "/home/lanforge") || (! -f "/home/lanforge/config.values" )) {
   error("* Unable to find /home/lanforge/config.values. Not configuring apache.");
   return;
}
my @config_values = `cat /home/lanforge/config.values`;
my @mgt_dev_lines = grep {/^mgt_dev/} @config_values;
if (@mgt_dev_lines != 1) {
   error("* mgt_dev misconfigured in config.values. Not configuring apache.");
   return;
}
my $mgt_dev = (split(/\s+/, $mgt_dev_lines[0]))[0];
if (!(defined $mgt_dev) || $mgt_dev eq "") {
   err("* Unable to find mgt_dev value. Not configuring apache.");
   return;
}

our $new_include;
our $httpconf;

# if we have a Listen directive in apache, comment it out and create an include
sub collectListenLines { # original httpd.conf, listen.conf
   my $conf = shift;
   my $new_include = shift;
   my @httpconf_lines = `cat $conf`;
   chomp(@httpconf_lines);
   my @new_httpconf_lines = ();
   my @new_listen_lines = ();
   my @listen_lines = grep {/^Listen /} @httpconf_lines;
   chomp(@listen_lines);
   my @include_lines = grep {m|^Include conf/lf_listen.conf$|} @httpconf_lines;
   chomp(@include_lines);

   if (@listen_lines < 1 ) {
      error(" * Apache misconfigured? No Listen directive and not include lf_listen.conf. Not modifying.");
      return;
   }

   for my $line (@httpconf_lines) {
      if ($line =~ /^Listen /) {
         $line = "# Moved to lf_listen.conf: $line";
         push(@listen_lines, "# $line");
      }
      push(@new_httpconf_lines, $line);
   }
} # ~collectListenLines

## ## ## ## ## ## ## ## ## ##
##          M A I N        ##
## ## ## ## ## ## ## ## ## ##

if ($is_fedora || $is_centos) {
   die("* Unable to find /etc/httpd/conf/httpd.conf. Not configuring apache.")
      unless( -f "/etc/httpd/conf/httpd.conf" );

   $::new_include = "/etc/httpd/conf/lf_listen.conf";
   $::httpconf = "/etc/httpd/conf/httpd.conf";
   if (-f $new_include) {
      print(" # lf_listen.conf already created, not creating\n");
      exit 0;
   }
   collectListenLines($::httpconf, $::new_include);
   exit 0;
} # ~fedora
elsif ($is_ubuntu) {
   $::new_include = "/etc/apache2/lf_listen.conf";
   $::httpconf = "/etc/apache2/ports.conf";
   die("* Unable to find $::httpconf. Not configuring apache.")
      unless ( -f $::httpconf );

   collectListenLines($::httpconf, $::new_include);
}
else {
   error("Configuring apache mgt port not configured on other systems.");
   exit 1;
}

# eof