#!/bin/bash

radio_list=(`ls -d /sys/class/ieee80211/*`)
sys_kd="/sys/kernel/debug/ieee80211"
for radio_path in "${radio_list[@]}"; do
    radio="${radio_path##*/}"
    #echo -n "$radio_path: $radio "
    echo -n "$radio "
    if [ -d "${sys_kd}/${radio}/ath9k/" ]; then
        echo "ath9k Vsta:200 APs:32 apclients:2048"
    elif [ -d "${sys_kd}/${radio}/ath10k/" ]; then
        # check for fwcfg file; if not there; assume 32vsta
        #echo "ath10k Vsta:64 APs:24 ap-clients:127"
        fwcfg_debug="${sys_kd}/${radio}/ath10k/firmware_info"
        if [ -r "$fwcfg_debug" ]; then
            fw_fname=""
            while IFS= read line; do
                if [[ x$line =~ xfwcfg: ]]; then
                    fw_fname=${line/fwcfg:/}
                fi
            done < $fwcfg_debug
            fw_fname=`echo $fw_fname`
            fw_fqp="/lib/firmware/ath10k/${fw_fname}"
            if [[ x${fw_fname} != x ]] && [ -r $fw_fqp ]; then
                vsta=0
                clients=0
                while read line; do
                    hunks=($line)
                    case "$line" in
                        vdevs*)
                            vsta="${hunks[2]}"
                            ;;
                        stations*)
                            clients="${hunks[2]}"
                            ;;
                    esac
                done < ${fw_fqp}
                echo "ath10 Vsta:${vsta} APs:24 ap-clients:${clients}"
            else
                echo "ath10k Vsta:32 APs:24 ap-clients:64 (assuming defaults)"
                echo "[${fw_fqp}] not found"
            fi
        else
            echo "ath10k Vsta:32 APs:24 ap-clients:64"
        fi
    else
        echo "other Vsta:1 APs:0 ap-clients:0"
    fi
done
