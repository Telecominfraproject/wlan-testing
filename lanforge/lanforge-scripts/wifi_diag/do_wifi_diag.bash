#!/bin/bash
# --------------------------------------------------------------------------- #
# do_wifi_diag.bash
#
# use this script process a pcap file to diagnose wifi characteristics.
# This calls the wifi_pcap_diag.pl script to do the real work.
#
# -o     Output directory name
# -f     Pcap file name
# -d     DUT mac (BSSID) address
# -C     (Clobber):  Remove output directory if it currently exists
#
# --------------------------------------------------------------------------- #
# scripts

# Check to make sure dependencies are installed
present=(
  gnuplot
  wkhtmltopdf
  tshark
)
killcommand=0
for i in "${present[@]}"; do
  present=`which $i | awk '{ print length }'`
  if [[ $present -gt 0 ]]; then
    :
  else
    killcommand=1
    echo "Please install $i on your system"
    exit 1
  fi
done
if [[ $killcommand -gt 0 ]]; then
  exit 1
else
  :
fi

output_dir=diag_report
input_fname=
dut=
clobber=0
show_help=0

while getopts "ho:f:d:C" arg; do
  #echo "ARG[$arg] OPTARG[$OPTARG]"
  case $arg in
  o)
    output_dir=$OPTARG
    ;;
  f)
    input_fname=$OPTARG
    ;;
  d)
    dut=$OPTARG
    ;;
  h)
    show_help=1
    ;;
  C)
    clobber=1
    ;;
  *)
    echo "Ignoring option $arg $OPTARG"
    ;;
  esac
done

if [ -z "$input_fname" -o -z "$dut" ]; then
  show_help=1
fi

if [ $show_help -gt 0 ]; then
  echo "Usage: $0 -f {input-pcap-file} -o {output-directory} -d {DUT-bssid}"
  echo " $0 -f my.pcap -o report -d dc:ef:09:e3:b8:7d"
  exit 1
fi

if [ -e $output_dir ]; then
  if [ $clobber = "1" ]; then
    echo "Removing existing output directory: $output_dir"
    rm -fr $output_dir
  else
    echo "ERROR:  Output directory: $output_dir already exists."
    exit 1
  fi
fi

mkdir -p $output_dir || exit 1

echo "Starting the wifi_pcap_diag.pl script, this can take a while...."
tshark -V -r $input_fname | ./wifi_pcap_diag.pl --report_prefix $output_dir --dut $dut >$output_dir/output.txt

echo "All done, open this file with a browser to view report: $output_dir/index.html"
exit 0
