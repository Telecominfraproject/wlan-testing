#!/bin/bash
set -x
./lf_associate_ap.pl -m ct524-genia.jbr --resource 1 --radio wiphy2 --action del_all_phy --port_del wiphy0
./lf_associate_ap.pl -m ct524-genia.jbr --resource 1 --radio wiphy2 --action del_all_phy --port_del wiphy1
./lf_associate_ap.pl -m ct524-genia.jbr --resource 1 --radio wiphy2 --action del_all_phy --port_del wiphy2
./lf_associate_ap.pl -m ct524-genia.jbr --resource 1 --radio wiphy2 --action del_all_phy --port_del wiphy3
sleep 5
while read line; do
   echo "Orphan: $line"
   hunks=($line)

   ./lf_portmod.pl -m ct524-genia.jbr --cmd delete --port_name "${hunks[1]}"
done < <(./lf_portmod.pl -m ct524-genia.jbr --resource 1 --list_port_names | grep sta)

sleep 5
echo "" > /tmp/clilog
now=`date +%Y-%m-%d-%H%M%S`
sudo tcpdump -eSni br0 -B 2048 -w "/tmp/dump-${now}" host ct524-genia.jbr.candelatech.com and port 4001 &
sleep 5
./lf_associate_ap.pl -m ct524-genia.jbr --resource 1 --radio wiphy2 --action add --security wpa2 \
  --ssid jedway-wpa2-x64-3-1 --passphrase jedway-wpa2-x64-3-1 --wifi_mode anAC --first_sta sta2000 \
  --first_ip DHCP --num_stations 30 --log_cli /tmp/clilog
sleep 1
sudo killall tcpdump
set +x
echo done
