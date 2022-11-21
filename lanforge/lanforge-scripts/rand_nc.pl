#!/usr/bin/perl
#-------------------------------------------------------------------
# FILE: rand_nc.pl
# AUTH: Daniel Berry - wizatta@hotmail.com
# VERS: 1.0 beta 4/07/04
# DESC: Simple perl script to generate random arguments for nc
#       TCP port connections.
#
# Command line arguments: None
#
# There are 3 arrays controlling target execution
# 
# @targ    = for storage of IP addresses or FQDN
# $targs   = set to number of targets in @targ
#
# @srcIP   = for storage of source IP addresses
# $srcIps  = set to number of source IP addresses
#
# @port    = for storage of the target TCP ports
# $ports   = set to the number of ports in @port
#
#   
#-------------------------------------------------------------------

# Target array - either IP address format or FQDN
@targ = ('box1.target.net','box2.target.net');
$targs = 2;

# Source IP address to use--should be assigned to system
@srcIP = ('10.1.1.1','10.1.1.2','10.1.1.3','10.1.1.4');
$srcIPs = 4;


# TCP port to connect to
@port = ('25','110','111','135','143','161','389','514','515','1080','1433','1521','8080');
$ports = 13;

# Set pause length for timing - seconds
$pausemin = 5;
$pausemax = 90;

#
# Create output log
   `echo "Netcat random TCP connection script..." >/tmp/nc_exe.log`;
   `date >>/tmp/nc_exe.log`;

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
        # Select source IP address
        my $sIPn = int(rand($srcIPs)); 
        $sIP = $srcIP[$sIPn];

        # 
        # Select target TCP port
        my $eport = int(rand($ports));
        $tport = $port[$eport];

        # Execute netcat connection from source IP to target IP and TCP port

        print "nc TCP Connect TARG: $i \t Src_IP: $sIP \t IP: $tgtip \t PORT: $tport \n";
        `echo "nc TCP Connect TARG: $i \t Src_IP: $sIP \t IP: $tgtip \t PORT: $tport">>/tmp/nc_exe.log`;

        `echo "^d"|/usr/bin/nc -v -w5 -s $sIP $tgtip $tport >>/tmp/nc_exe.log`;


	$i++;
        $pause = $pausemin + int(rand($pausemax));
        print "Sleeping $pause ...\n";
        
        sleep $pause;
}

#
# End - script will terminate normally if all works correctly
#
#-------------------------------------------------------------------
