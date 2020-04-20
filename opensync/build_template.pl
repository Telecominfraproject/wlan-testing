#!/usr/bin/perl

use strict;
use warnings;
use Getopt::Long;

my $ch2 = 1;
my $ch5lo = 44;
my $ch5hi = 108;
my $ssid2 = "Connectus-local";
my $ssid5 = "Connectus-local-5";
my $encr2 = "WPA-PSK";
my $encr5 = "WPA-PSK";
my $key2 = "12345678";
my $key5 = "12345678";
my $country = "CA";
my $help = 0;

my $usage = qq($0
  [--country {2-letter country code: CA, US, DE, ...]   # Default is CA
  [--ch2 {2.4Ghz channel}]               # Default is 1
  [--ch5lo {Low 6Ghz channel}]           # Default is 44
  [--ch5hi {High 6Ghz channel}]          # Default is 108
  [--ssid2 {SSID for 2.4Ghz radio}]      # Default is Connectus-local
  [--ssid5 {SSID for 5Ghz radio}]        # Default is Connectus-local-5
  [--encr2 {Encryption type for 2.4Ghz radio}]  # Default is WPA-PSK
  [--encr5 {Encryption type for 5Ghz radio}]    # Default is WPA-PSK
  [--key2  {Encryption key (password) for 2.4Ghz radio}]  # Default is 12345678
  [--key5  {Encryption key (password) for 5Ghz radio}]    # Default is 12345678

Example:
$0 --ssid2 test-ssid2 --ssid5 test-ssid5 < template_2_ssids.json > mytemplate.json

$0 --country US --ch2 6 --ch5lo 36 --ch5hi 100 --key2 abcdefgh2 --key5 abcdefgh5 --ssid2 ben --ssid5 ben5 < template_2_ssids.json
);

GetOptions
(
  'country=s'                 => \$country,
  'ch2=s'                     => \$ch2,
  'ch5lo=s'                   => \$ch5lo,
  'ch5hi=s'                   => \$ch5hi,
  'ssid2=s'                   => \$ssid2,
  'ssid5=s'                   => \$ssid5,
  'encr2=s'                   => \$encr2,
  'encr5=s'                   => \$encr5,
  'key2=s'                    => \$key2,
  'key5=s'                    => \$key5,
  'help|?'                    => \$help,
) || (print($usage) && exit(1));

if ($help) {
  print($usage) && exit(0);
}

while (<>) {
   my $ln = $_;
   chomp($ln);

   $ln =~ s/__COUNTRY_CODE__/$country/g;
   $ln =~ s/__CH2__/$ch2/g;
   $ln =~ s/__CH5L__/$ch5lo/g;
   $ln =~ s/__CH5H__/$ch5hi/g;
   $ln =~ s/__SSID2__/$ssid2/g;
   $ln =~ s/__SSID5__/$ssid5/g;
   $ln =~ s/__ENCRYPT2__/$encr2/g;
   $ln =~ s/__ENCRYPT5__/$encr5/g;
   $ln =~ s/__PSK2__/$key2/g;
   $ln =~ s/__PSK5__/$key5/g;

   print "$ln\n";
}

exit 0;
