#!/usr/bin/perl

# Un-buffer output
$| = 1;

use strict;


my $sleep_time = 30;
my $vlans = 100;
my $ip_base = "192.168.10";
my $gw = "192.168.10.1";
my $lsb_start = 10;
my $eth_dev = "eth0";
my $vid_base = 1000;
my $i;
my $vid;
my @pids = ();
my $peer = 0;

if ($ARGV[0] eq "p") {
  # when running on peer machine...
  print "Running in peer mode..\n";
  $peer = 1;
  $lsb_start += $vlans;
  $gw = "192.168.10.250";
}

#`rmmod 8021q`;
#`modprobe 8021q`;
my $loop = 0;
while (1) {
  print "Creating and configuring vlans..loop: $loop\n";
  for ($i = 0; $i<$vlans; $i++) {
    $vid = $vid_base + $i;
    my $v = "$eth_dev.$vid";
    my $lsb = $lsb_start + $i;
    #print "Creating & configuring VLAN: $eth_dev.$vid\n";
    `vconfig add $eth_dev $vid`;
    #my $cmd = "ifconfig $v $ip_base.$lsb netmask 255.255.255.0 up";
    #print "Configuring with command -:$cmd:-\n";
    #`$cmd`;

    my $tbl = $i + 1;

    printAndExec("ip link set $v down");
    printAndExec("ip link set $v up");
    printAndExec("ip addr flush dev $v > /dev/null 2>&1");
    printAndExec("ip address add $ip_base.$lsb/24 broadcast $ip_base.255 dev $v");
    printAndExec("ip link set dev $v up");
    printAndExec("ip ru add from $ip_base.$lsb/32 table $tbl");
    printAndExec("ip route add $ip_base.0/24 via $ip_base.$lsb table $tbl");
    printAndExec("ip route add 0/0 via $gw dev $v table $tbl");
    printAndExec("echo 1 > /proc/sys/net/ipv4/conf/$v/arp_filter");

    # Start traffic on interface
    my $kidpid;
    if (!defined($kidpid = fork())) {
      # fork returned undef, so failed
      die "Cannot fork: $!";
    } elsif ($kidpid == 0) {
      # fork returned 0, so this branch is child
      while (1) {
	my $url;
	if ($peer) {
	  my $mip = $lsb - $vlans;
	  $url = "http://$ip_base.$mip/index.html";
	}
	else {
	  my $mip = $lsb + $vlans;
	  $url = "http://$ip_base.$mip/index.html";
	  #print "url: $url\n";
	}

	my $curl_cmd = "curl --interface $eth_dev.$vid --url $url -o $eth_dev.$vid.index.html > /dev/null 2>&1";
	#print "Child process running: $curl_cmd\n";
	system("$curl_cmd");
	sleep(5);
      }
    } else {
      # fork returned 0 nor undef
      # so this branch is parent
      @pids = (@pids, $kidpid);
      # waitpid($kidpid, 0);
    }
  }

  my $slp = (rand() * 1000000) % $sleep_time;
  if ($slp < 3) {
    $slp = 3;
  }
  print "  Done creating vlans and starting curl processes, sleeping $slp seconds.\n";
  # Sleep a while to wait for curl to do it's thing
  sleep($slp);

  print "  Removing all VLANs.\n";
  for ($i = 0; $i<$vlans; $i++) {
    $vid = $vid_base + $i;
    #print "Removing vlan: $eth_dev.$vid\n";
    `vconfig rem $eth_dev.$vid`;
  }#for

  print "  Killing all curl instances.\n";
  for ($i = 0; $i<@pids; $i++) {
    `kill -9 $pids[$i]`;
  }

  print "  Done with loop: $loop\n";
  $loop++;
}# while



sub printAndExec {
  my $cmd = $_[0];

  #print "$cmd\n";
  # NOTE:  If you use the single back-ticks here, it will hang, probably some
  #   signal problem...never figured out why really (ERESTARTSYS) was the error
  #   that perl hung on... --Ben
  system("$cmd");
}

