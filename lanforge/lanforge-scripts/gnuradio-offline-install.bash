#!/bin/bash

[ ! -f urls_file.txt ] && echo "Where is urls_list.txt?" && exit 1
DLD=/home/lanforge/Downloads
installed_list=()
already_downloaded_list=()
not_found_list=()
candidate_list=()

while read L; do
    # echo "$L"
    bzname=`basename $L`
    short=${bzname%.fc30*}
    if [[ x$short = x ]]; then
        echo "bad substitution on $L"
        continue
    fi
    echo -n "Looking for $short"

    rez=`rpm -qa ${short}*`
    # echo "result $?"
    if [[ x$rez = x ]]; then
        echo -n "$bzname is not installed"
        if compgen -G "${DLD}/${bzname}"; then
            echo " already downloaded"
            already_downloaded_list+=($bzname);
        else
            wget -q -O "${DLD}/${bzname}" "$L"
            if (( $? != 0 )); then
                letterurl="${L%/*}/"
                needle="${short:0:13}"
                echo -n " need to look for ${letterurl}${needle} ..."
                some_match=`curl -sq "${letterurl}" | grep -- "$needle"`
                if (( $? != 0 )) || [[ x$some_match = x ]]; then
                    echo "Unable to find $short"
                    not_found_list+=("$L")
                else
                    echo "possible candidate"
                    candidate_list+=("$some_match")
                fi
            fi
        fi
    fi
done < urls_file.txt
echo ""
echo "Installed list: "
printf "%s, " "${installed_list[@]}"

echo ""
echo "Already downloaded list: "
printf "    %s\\n" "${already_downloaded_list[@]}"

echo ""
echo "Not found list: "
printf "    %s\\n" "${not_found_list[@]}"

echo ""
echo "Candidate list: "
printf "    %s\\n" "${candidate_list[@]}"


echo "done."