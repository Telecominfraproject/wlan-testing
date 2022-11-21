#!/usr/bin/perl
#-------------------------------------------------------------------
# FILE: rand_nmap.pl
# AUTH: Daniel Berry - wizatta@hotmail.com
# VERS: 1.2 beta 3/08/04
# DESC: Simple perl script to generate random arguments for nmap
#       scans. 
#
# NOTE: For use with LANforge 4-port traffic generators using
#       standard nmap executable.
#
# Command line arguments: None
#
# There are 2 arrays controlling target execution
# 
# @targ    = for storage of IP addresses of FQDN
# $targs   = set to number of targets in @targ
#
# @port    = for storage of the local ethernet ports
# $ports   = set to the number of ports in @port
#
#   
#-------------------------------------------------------------------

# Target array - either IP address format or FQDN
@targ = ('10.1.1.1-254','10.1.2.1-254');
$targs = 2;

# Ethernet port to use (eth1-4)
@port = ('eth4#1','eth4#2','eth4#3');
$ports = 3;

# Set pause length for timing - seconds
$pause = 1800;

#
# Setup loop -- loop is continious until terminated
#
my $i = 0;
while (1) {
        # 
        # Random selection of target
        my $tgt = int(rand($targs));
        $tgtip = $targ[$tgt]; 

        # 
        # Select source eth port
        my $eport = int(rand($ports));
        $srcport = $port[$eport];

        # Execute nmap TCP Connect scan from source port to target

        print "nmap TCP Connect scan TARG: $i \t IP: $tgtip \t ETH: $srcport  \n";

        $stuff = `/usr/bin/nmap -e $srcport -sT -o /tmp/nmap_exe.log $tgtip`;
     
        # Write output of execution to log
        open (FILE, ">/tmp/nmap.log");
             print FILE $stuff;
        close (FILE);

	$i++;
        print "Sleeping $pause ...\n";
        sleep $pause;
}

#
# End - script will terminate normally if all works correctly
#
#-------------------------------------------------------------------
