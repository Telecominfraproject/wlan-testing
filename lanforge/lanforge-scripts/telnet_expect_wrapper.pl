#!/usr/bin/perl

my $i = 0;
while (1) {
	`/home/lanforge/telnet.expect`;
	print "Completed telnet connection $i\n";
	$i++;
}

