#!/bin/bash
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
#      Check for large files and purge the ones requested                                               #
#                                                                                                       #
# The -a switch will automatically purge core files when there                                          #
# is only 5GB of space left on filesystem.                                                              #
#                                                                                                       #
# To install as a cron-job, add the following line to /etc/crontab:                                     #
# 1 * * * *  root /home/lanforge/scripts/check_large_files.sh -a 2>&1 | logger -t check_large_files     #
#                                                                                                       #
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
# set -x
# set -e
# these are default selections
selections=()
show_menu=1
verbose=0
quiet=0
starting_dir="$PWD"
cleanup_size_mb=$(( 1024 * 5 ))
# do not name this file "core_x" because it will get removed
lf_core_log="/home/lanforge/found_cores_log.txt"

USAGE="$0 # Check for large files and purge many of the most inconsequencial
 -a   # automatic: quietly empty trash and remove crash files if free space is < ${cleanup_size_mb}MB
 -b   # remove extra kernels and modules
 -c   # remove all core files
 -d   # remove old LANforge downloads
 -h   # help
 -k   # remove ath10k crash files
 -l   # remove old files from /var/log, truncate /var/log/messages
 -m   # remove orphaned fileio items in /mnt/lf
 -q   # quiet
 -r   # compress /home/lanforge report data and pcap files
 -s   # empty the trash
 -t   # remove /var/tmp files
 -v   # verbose
 -z   # compressed files in /home/lanforge
"

eyedee=`id -u`
if (( eyedee != 0 )); then
    echo "$0: Please become root to use this script, bye"
    exit 1
fi

debug() {
    if [[ x$verbose = x ]] || (( $verbose < 1 )); then return; fi
    echo ": $1"
}

note() {
    if (( $quiet > 0 )); then return; fi
    echo "# $1"
}

function contains() {
    if [[ x$1 = x ]] || [[ x$2 = x ]]; then
        echo "contains wants ARRAY and ITEM arguments: if contains name joe; then...  }$"
        exit 1
    fi
    # these two lines below are important to not modify
    local tmp="${1}[@]"
    local array=( ${!tmp} )

    # if [[ x$verbose = x1 ]]; then
    #    printf "contains array %s\n" "${array[@]}"
    # fi
    if (( ${#array[@]} < 1 )); then
        return 1
    fi
    local item
    for item in "${array[@]}"; do
        # debug "contains testing $2 == $item"
        [[ "$2" = "$item" ]] && return 0
    done
    return 1
}

function remove() {
    if [[ x$1 = x ]] || [[ x$2 = x ]]; then
        echo "remove wants ARRAY and ITEM arguments: if contains name joe; then...  }$"
        exit 1
    fi
    # these two lines below are important to not modify
    local tmp="${1}[@]"
    local array=( ${!tmp} )

    # if [[ x$verbose = x1 ]]; then
    #    printf "contains array %s\n" "${array[@]}"
    # fi
    if (( ${#array[@]} < 1 )); then
        return 1
    fi
    local item
    for i in "${!array[@]}"; do
        if [[ ${array[$i]} = "$2" ]]; then
            unset 'array[i]'
            debug "removed $2 from $1"
            return 0
        fi
    done
    return 1
}

function disk_space_below() {
    if [[ x$1 = x ]] || [[ x$2 = x ]]; then
        echo "disk_free: needs to know what filesystem, size in bytes to alarm on"
        return
    fi
    local amount_left_mb=`df -BM --output=iavail | tail -1`
    if (( $amount_left_mb < $cleanup_size_mb )) ; then
        debug "amount left $amount_left_mb lt $cleanup_size_mb"
        return 0
    fi
    debug "amount left $amount_left_mb ge $cleanup_size_mb"
    return 1
}

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
# ----- ----- M A I N                                   ----- ----- #
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

#opts=""
opts="abcdhklmqrtv"
while getopts $opts opt; do
  case "$opt" in
    a)
      if contains "selections" "v"; then
          verbose=1
      else
          verbose=0
      fi
      quiet=1
      selections+=($opt)
      selections+=(s) # dump trash
      show_menu=0
      ;;
    b)
      selections+=($opt)
      ;;
    c)
      selections+=($opt)
      ;;
    d)
      selections+=($opt)
      ;;
    h)
      echo "$USAGE"
      exit 0
      ;;
    k)
      selections+=($opt)
      ;;
    l)
      selections+=($opt)
      ;;
    m)
      selections+=($opt)
      ;;
    r)
      selections+=($opt)
      ;;
    s)
      selections+=($opt)
      ;;
    q)
      quiet=1
      verbose=0
      ;;
    t)
      selections+=($opt)
      ;;
    v)
      quiet=0
      verbose=1
      ;;
    z)
      selections+=($opt)
      ;;
    *)
      echo "unknown option: $opt"
      echo "$USAGE"
      exit 1
      ;;
  esac
done

#if (( ${#selections} < 1 )); then
#  echo "$USAGE"
#  exit 0
#fi

HR=" ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----"
function hr() {
  echo "$HR"
}

declare -A totals=(
    [b]=0
    [c]=0
    [d]=0
    [k]=0
    [l]=0
    [m]=0
    [r]=0
    [s]=0
    [t]=0
    [z]=0
)
declare -A desc=(
    [b]="kernel files"
    [c]="core files"
    [d]="lf downloads"
    [k]="lf/ath10 files"
    [l]="/var/log"
    [m]="/mnt/lf files"
    [n]="dnf cache"
    [r]="report data"
    [s]="trash can"
    [t]="/var/tmp"
    [z]="compressed files"
)
declare -A surveyors_map=(
    [b]="survey_kernel_files"
    [c]="survey_core_files"
    [d]="survey_lf_downloads"
    [k]="survey_ath10_files"
    [l]="survey_var_log"
    [m]="survey_mnt_lf_files"
    [n]="survey_dnf_cache"
    [r]="survey_report_data"
    [s]="survey_trash_can"
    [t]="survey_var_tmp"
    [z]="survey_compressed_files"
)

declare -A cleaners_map=(
    [b]="clean_old_kernels"
    [c]="clean_core_files"
    [d]="clean_lf_downloads"
    [k]="clean_ath10_files"
    [l]="clean_var_log"
    [m]="clean_mnt_lf_files"
    [n]="clean_dnf_cache"
    [r]="compress_report_data"
    [s]="empty_trash_can"
    [t]="clean_var_tmp"
    [z]="clean_compressed_files"
)

kernel_to_relnum() {
    #set -euxv
    local hunks=()
    # 1>&2 echo "KERNEL RELNUM:[$1]"
    local my1="${1/*[^0-9]-/}" # Dang, this is not intuitive to a PCRE user
    #1>&2 echo "KERNEL [$1] REGEX:[$my1]"
    my1="${my1//\+/}"
    if [[ $my1 =~ ^[^0-9] ]]; then
        1>&2 echo "BAD SERIES: [$1]"
        exit 1
    fi
    IFS="." read -ra hunks <<< "$my1"
    IFS=
    local tmpstr
    local max_width=8
    local last_len=0
    local expandos=()
    for i in 0 1 2; do
        if (( $i < 2 )); then
            #1>&2 echo "HUNK $i: [${hunks[$i]}]"
            expandos+=( $(( 100 + ${hunks[$i]} )) )
        else
            tmpstr="00000000${hunks[i]}"
            last_len=$(( ${#tmpstr} - $max_width ))
            expandos+=( ${tmpstr:$last_len:${#tmpstr}} )
            #1>&2 echo "TRIMMED ${tmpstr:$last_len:${#tmpstr}}"
        fi
    done

    set +x
    #1>&2 echo "EXPANDO: ${expandos[0]}${expandos[1]}${expandos[2]}"
    echo "k${expandos[0]}${expandos[1]}${expandos[2]}"
}

empty_trash_can() {
    #set -vux
    if [ -x /usr/bin/trash-empty ]; then
        for can in "${trash_cans[@]}"; do
            if [[ $can = /home* ]]; then
                # that =() nonsense is turning the '/' into spaces and letting default IFS let () treat it as array items
                local hunks=(${can//\// })
                local uzer="${hunks[1]}"
                su -l $uzer -c "unset DISPLAY; /usr/bin/trash-empty"
            else
                # we should be root
                /usr/bin/trash-empty
            fi
        done
    else
        note "trash-cli not installed, destroying trash files"
        for can in "${trash_cans[@]}"; do
            find "${can}" -type f -exec rm -vf {} \;
        done
    fi
    totals[s]=0
    set +vux
}

clean_compressed_files() {
    note "Listing compressed files..."
    local f
    if (( ${#compressed_files[@]} > 0 )); then
        for f in "${compressed_files[@]}"; do
            echo "$f"
        done | paste - - - | less
    else
        echo "No compressed files."
    fi
    totals[z]=0
}
clean_old_kernels() {
    note "Cleaning old CT kernels..."
    local f
    if (( ${#removable_packages[@]} > 0 )); then
        for f in "${removable_packages[@]}"; do
            echo "$f\*"
        done | xargs /usr/bin/rpm --nodeps -hve
    fi
    if (( ${#removable_kernels[@]} > 0 )); then
        for f in "${removable_kernels[@]}"; do
            echo "$f"
        done | xargs rm -f
    fi

    if (( ${#removable_libmod_dirs[@]} > 0 )); then
        printf "        removable_libmod_dirs[/lib/modules/%s]\n" "${removable_libmod_dirs[@]}"
        for f in "${removable_libmod_dirs[@]}"; do
            echo "/lib/modules/$f"
        done | xargs rm -rf
    fi
    # check to see if there are 50_candela-x files that
    # lack a /lib/modules directory
    local fifty_files=(`ls /etc/grub.d/50_candela_*`)
    local k_v
    for file in "${fifty_files[@]}"; do
        k_v=${file#/etc/grub.d/50_candela_}
        #echo "K_V[$k_v]"
        if [ ! -d /lib/modules/$k_v ]; then
            echo "/lib/modules/$k_v not found, removing /etc/grub.d/50_candela_$k_v"
            rm -f "/etc/grub.d/50_candela_${k_v}"
        fi
    done

    grub2-mkconfig -o /boot/grub2/grub.cfg

    if [ -d "/boot2" ]; then
        rm -rf /boot2/*
        rsync -a /boot/. /boot2/
        local dev2=`df /boot2/ |awk '/dev/{print $1}'`
        if [ x$dev2 != x ]; then
            /usr/sbin/grub2-install $dev2 ||:
        fi
    fi
}

clean_core_files() {
    note "Cleaning core files..."
    if (( ${#core_files[@]} < 1 )); then
        debug "No core files ?"
        return 0
    fi

   local counter=0
    if [ ! -f "$lf_core_log" ]; then
        touch "$lf_core_log"
    fi
    date +"%Y-%m-%d-%H:%M.%S" >> $lf_core_log
    for f in "${core_files[@]}"; do
        file "$f" >> "$lf_core_log"
    done
    note "Recorded ${#core_files[@]} core files to $lf_core_log: "
    tail -n $(( 1 + ${#core_files[@]} )) $lf_core_log
    local do_delete=0
    if contains "selections" "a"; then
        disk_space_below /      $cleanup_size_mb && do_delete=$(( $do_delete + 1 ))
        disk_space_below /home  $cleanup_size_mb && do_delete=$(( $do_delete + 1 ))
        (( $do_delete > 0)) && note "disk space below $cleanup_size_mfb, removing core files"
    elif contains "selections" "c"; then
        do_delete=1
        note "core file cleaning selected"
    fi
    if (( $do_delete > 0 )); then
        for f in "${core_files[@]}"; do
            echo -n "-"
            rm -f "$f" && remove "core_files" "$f"
            counter=$(( counter + 1 ))
            if (( ($counter % 100) == 0 )); then
                sleep 0.2
            fi
        done
    else
        note "disk space above $cleanup_size_mb, not removing core files"
    fi
    #set +vux
    echo ""
    totals[c]=0
    survey_core_files
}

clean_lf_downloads() {
    if (( ${#lf_downloads[@]} < 1 )); then
        note "No /home/lanforge/downloads files to remove"
        return 0
    fi
    note "Clean LF downloads..."
    if (( $verbose > 0 )); then
        echo "Would Delete: "
        printf "[%s] " "${lf_downloads[@]}" | sort
    fi
    cd /home/lanforge/Downloads
    for f in "${lf_downloads[@]}"; do
        [[ "$f" = "/" ]] && echo "Whuuut? this is not good, bye." && exit 1
        # echo "Next:[$f]"
        sleep 0.02
        rm -f "$f"
    done
    totals[d]=0
    cd "$starting_dir"
}

clean_ath10_files() {
    note "clean_ath10_files WIP"
    local f
    while read f; do
        echo "removing $f"
        rm -f "$f"
    done < <( find /home/lanforge -type f -iname "ath10*" ||:)
}

clean_var_log() {
    note "Vacuuming journal..."
    journalctl --vacuum-size 1M
    if (( ${#var_log_files[@]} < 1 )); then
        note "No notable files in /var/log to remove"
        return
    fi
    local vee=""
    if (( $verbose > 0 )); then
        printf "%s\n" "${var_log_files[@]}"
        vee="-v"
    fi
    cd /var/log
    while read file; do
        if [[ $file = /var/log/messages ]]; then
            echo "" > /var/log/messages
        else
            rm -f $vee "$file"
        fi
    done <<< "${var_log_files[@]}"
    cd "$starting_dir"
}

clean_dnf_cache() {
    local yum="dnf"
    which --skip-alias dnf &> /dev/null
    (( $? < 0 )) && yum="yum"
    debug "Purging $yum cache"
    $yum clean all
    totals[n]=0
}

clean_mnt_lf_files() {
    note "cleaning mnt lf files..."
    if (( $verbose > 0 )); then
        printf "%s\n" "${mnt_lf_files[@]}"
    fi
    rm -f  "${mnt_lf_files[@]}"
    totals[m]=0
}

compress_report_data() {
    note "compress report data..."
    cd /home/lanforge
    # local csvfiles=( $( find /home/lanforge -iname "*.csv"  -print0 ))
    local vile_list=(`find html-reports/ lf_reports/ report-data/ tmp/ -type f \
         -a \( -name '*.csv' -o -name '*.pdf' -o -name '*.pdf' -o -name '*.pcap'  -o -name '*.pcapng' \)`)
    counter=1
    for f in "${vile_list[@]}"; do
        (( $verbose > 0 )) && echo "    compressing $f" || echo -n " ${counter}/${#vile_list[@]}"
        nice xz -T0 -5 "$f"
        (( counter+=1 ))
    done
    totals[r]=0
    cd -
    echo ""
}

clean_var_tmp() {
    note "clean var tmp"
    if (( $verbose > 0 )); then
        printf "    %s\n" "${var_tmp_files[@]}"
        sleep 1
    fi
    for f in "${var_tmp_files[@]}"; do
        rm -f "$f"
        sleep 0.2
    done
}

kernel_files=()         # temp
lib_module_dirs=()      # temp
declare -A kernel_sort_names
declare -A pkg_sort_names
declare -A libmod_sort_names
removable_kernels=()    # these are for CT kernels
removable_libmod_dirs=() # these are for CT kernels
removable_packages=()   # these are for Fedora kernels
removable_pkg_series=()
survey_kernel_files() {
    unset removable_kernels
    unset removable_libmod_dirs
    unset removable_packages
    unset lib_module_dirs
    unset kernel_sort_names
    unset kernel_sort_serial
    unset pkg_sort_names
    unset libmod_sort_names
    declare -A kernel_sort_serial=()
    declare -A kernel_sort_names=()
    declare -A pkg_sort_names=()
    declare -A libmod_sort_names=()
    local ser
    local file
    debug "Surveying Kernel files"
    mapfile -t kernel_files < <(find /boot -maxdepth 1 -type f -a \( \
        -iname "System*" -o -iname "init*img" -o -iname "vm*" -o -iname "ct*" \) \
        2>/dev/null | grep -v rescue | sort)
    mapfile -t lib_module_dirs < <(find /lib/modules -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort)
    local booted=`uname -r`

    note "** You are running kernel $booted **"

    local file
    local fiile
    for file in "${kernel_files[@]}"; do
        debug "kernel_file [$file]"
        [[ $file =~ /boot/initramfs* ]] && continue
        [[ $file =~ *.fc*.x86_64 ]] && continue
        [[ $file = *initrd-plymouth.img ]] && continue
        fiile=$( basename $file )
        fiile=${fiile%.img}

        if [[ $fiile =~ $booted ]]; then
            debug "    ignoring booted CT kernel $file"
            # sleep 2
            continue
        else
            ser=$( kernel_to_relnum ${fiile#*ct} )
            kernel_sort_serial[$ser]=1
            # debug "file[$file] ser[$ser]"
            kernel_sort_names["$file"]="$ser"
            removable_kernels+=($file)
        fi
    done
    # sleep 2
    local booted_ser=$( kernel_to_relnum $booted )
    if (( ${#kernel_sort_names[@]} > 0 )); then
        declare -A ser_files
        for file in "${!kernel_sort_names[@]}"; do
            ser="${kernel_sort_names[$file]}"
        done
        debug "Removable CT kernels:"
        while read ser; do
            (( $verbose > 0 )) && printf "    kernel file [%s]\n" "${kernel_sort_names[$ser]}"
            removable_kernels+=(${kernel_sort_names["$ser"]})
        done < <(echo  "${!kernel_sort_names[@]}" | sort | head -n -1)
    fi

    debug "Module directories elegible for removal: "
    for file in "${lib_module_dirs[@]}"; do
        file=${file#/lib/modules/}
        # debug "/lib/modules/ ... $file"
        if [[ $file =~ $booted ]]; then
            debug "     Ignoring booted module directory $file"
            continue
        elif [[ $file = *.fc??.x86_64 ]]; then
            debug "     Ignoring Fedora module directory $file"
            continue
        else
            ser=$( kernel_to_relnum $file )
            # debug "     eligible [$ser] -> $file"
            libmod_sort_names[$ser]="$file"
        fi
    done

    if (( ${#libmod_sort_names[@]} > 0 )); then
        # debug "Removable libmod dirs: "
        while read ser; do
            file="${libmod_sort_names[$ser]}"
            # debug "     $ser -> $file"
            if [[ $file =~ $booted ]]; then
                debug "     Ignoring booted $booted module directory $file"
                continue
            fi
            removable_libmod_dirs+=( "$file" )
            # echo "    [$ser][${libmod_sort_names[$ser]}] -> $file"
        done < <( printf "%s\n" "${!libmod_sort_names[@]}" | sort | uniq)
        # we don't need to sort these ^^^ because they were picked out near line 419
    fi
    #if (( $verbose > 0 )); then
    #    printf " removable_libmod_dirs: %s\n" "${removable_libmod_dirs[@]}"
    #fi
    # set +veux

    local boot_image_sz=$(du -hc "${kernel_files[@]}" | awk '/total/{print $1}')
    local lib_dir_sz=$(du -hc "${lib_module_dirs[@]}" | awk '/total/{print $1}')
    totals[b]="kernels: $boot_image_sz, modules: $lib_dir_sz"

    local pkg
    local k_pkgs=()
    removable_pkg_series=()

    # need to avoid most recent fedora kernel
    if [ ! -x /usr/bin/rpm ]; then
        note "Does not appear to be an rpm system."
        return 0
    fi
    local ur=$( uname -r )
    local kern_pkgs=( $( rpm -qa 'kernel*' | sort ) )
    local ser
    local zpkg
    declare -A pkg_to_ser
    for pkg in "${kern_pkgs[@]}"; do
        if [[ $pkg = kernel-tools-* ]] \
            || [[ $pkg = kernel-headers-* ]] \
            || [[ $pkg = kernel-devel-* ]] ; then
            continue
        fi
        if [[ $pkg =~ $booted ]]; then
            debug "     ignoring current kernel [$pkg]"
            continue
        fi
        k_pkgs+=( $pkg )
    done

    for pkg in "${k_pkgs[@]}"; do
        zpkg="$pkg"
        zpkg=${pkg##kernel-modules-extra-}
        zpkg=${pkg##kernel-modules-}
        zpkg=${pkg##kernel-core-}
        zpkg=${pkg%.fc??.x86_64}

        if [[ $zpkg =~ $booted ]]; then
            continue
        fi
        kernel_series=$( kernel_to_relnum ${zpkg##kernel-} )

        pkg_to_ser[$pkg]="$kernel_series"
        pkg_sort_names[$kernel_series]=1
    done

    while read ser; do
        # debug "    can remove series [$ser] "
        removable_pkg_series+=($ser)
    done < <( printf "%s\n" "${!pkg_sort_names[@]}" | sort | head -n -1)

    for pkg in "${k_pkgs[@]}"; do
        pkg=${pkg%.fc??.x86_64}
        ser=$( kernel_to_relnum $pkg )
        if (( ${#removable_pkg_series[@]} > 0 )); then
            for zpkg in "${removable_pkg_series[@]}"; do
                if (( $ser == $zpkg )); then
                    removable_packages+=($pkg)
                fi
            done
        fi
    done

    set +x
    if (( $quiet < 1 )); then
        if [[ ${removable_packages+x} = x ]] && (( ${#removable_packages[@]} > 0 )); then
            echo "Removable packages "
            printf "    %s\n" "${removable_packages[@]}"
        fi
        if [[ ${removable_kernels+x} = x ]] && (( ${#removable_kernels[@]} > 0 )); then
            echo "Removable kernel files "
            printf "    %s\n" "${removable_kernels[@]}"
        fi
        if [[ ${removable_libmod_dirs+x} = x ]] && (( ${#removable_libmod_dirs[@]} > 0 )); then
            echo "Removable /lib/module directories "
            printf "    %s\n" "${removable_libmod_dirs[@]}"
        fi
    fi
} # ~survey_kernel_files

# check the trash can
trash_cans=()
survey_trash_can() {
    debug "Checking trash can"
    local lstf=".local/share/Trash/files"
    local some_items=()
    mapfile -t trash_cans < <(ls -d /root/$lstf /home/lanforge/$lstf 2>/dev/null) 2>/dev/null
    if [[ $verbose = 1 ]] && (( ${#trash_cans} > 0 )); then
        printf "    %s\n" "${trash_cans[@]}"
    fi
    if (( ${#trash_cans[@]} > 0 )); then
        totals[s]=$( du -hc "${trash_cans[@]}" | awk '/total/{print $1}' )
        [[ x${totals[s]} = x ]] && totals[s]=0 ||:
        for can in "${trash_cans[@]}"; do
            mapfile -t -O "${#some_items[@]}" some_items < <(find "$can" -type f | head 2>/dev/null )
        done
    fi
    if (( ${#some_items[@]} > 0 )) && (( $quiet < 1 )) && (( $verbose > 0 )); then
        hr
        note "Some trash can items:"
        note "${some_items[@]}"
        hr
        # sleep 1
    fi
    if [ ! -x /usr/bin/trash-empty ] && (( $quiet < 1 )); then
        note "Package trash-cli not installed. Please install it using command:"
        note "sudo dnf install -y trash-cli"
        sleep 2
    fi
}

# Find core files
core_files=()
survey_core_files() {
    debug "Surveying core files"
    cd /

    mapfile -t core_files < <(ls /core* /home/lanforge/core* 2>/dev/null) 2>/dev/null
    if [[ $verbose = 1 ]] && (( ${#core_files[@]} > 0 )); then
        printf "    %s\n" "${core_files[@]}" | head
    fi
    if (( ${#core_files[@]} > 0 )); then
        totals[c]=$(du -hc "${core_files[@]}" | awk '/total/{print $1}')
        [[ x${totals[c]} = x ]] && totals[c]=0 ||:
    else
        totals[c]=0
    fi

    cd "$starting_dir"
}

# downloads
lf_downloads=()
survey_lf_downloads() {
    debug "Surveying /home/lanforge downloads"
    [ ! -d "/home/lanforge/Downloads" ] && note "No downloads folder " && return 0
    cd /home/lanforge/Downloads
    mapfile -t lf_downloads < <(ls *gz *z2 *-Installer.exe *firmware* kinst_* *Docs* 2>/dev/null)
    if [[ ${lf_downloads+x} = x ]]; then
        totals[d]=$(du -hc "${lf_downloads[@]}" | awk '/total/{print $1}')
        [[ x${totals[d]} = x ]] && totals[d]=0
    else
        totals[d]=0
    fi
    cd "$starting_dir"
}

# Find ath10k crash residue
ath10_files=()
survey_ath10_files() {
    debug "Surveying ath10 crash files"
    mapfile -t ath10_files < <(ls /home/lanforge/ath10* 2>/dev/null)
    if [[ ${ath10_files+x} = x ]]; then
        totals[k]=$(du -hc "${ath10_files[@]}" 2>/dev/null | awk '/total/{print $1}')
        [[ x${totals[k]} = x ]] && totals[k]=0 ||:
    else
        totals[k]=0
        return
    fi

}

# stuff in var log
var_log_files=()
survey_var_log() {
    debug "Surveying var log"
    mapfile -t var_log_files < <(find /var/log -type f -size +35M \
        -not \( -path '*/journal/*' -o -path '*/sa/*' -o -path '*/lastlog' \) 2>/dev/null ||:)
    if [[ ${var_log_files+x} = x ]]; then
        totals[l]=$(du -hc "${var_log_files[@]}" 2>/dev/null | awk '/total/{print $1}' )
        [[ x${totals[l]} = x ]] && totals[l]=0 ||:
    else
        totals[l]=0
        return
    fi
}

# stuff in var tmp
var_tmp_files=()
survey_var_tmp() {
    debug "Surveying var tmp"
    mapfile -t var_tmp_files < <(find /var/tmp -type f 2>/dev/null || :)
    if [[ ${var_tmp_files+x} = x ]]; then
        totals[t]=$(du -sh "${var_tmp_files[@]}" 2>/dev/null | awk '/total/{print $1}' )
        [[ x${totals[t]} = x ]] && totals[t]=0 ||:
    else
        totals[t]=0
    fi
}

# Find size of /mnt/lf that is not mounted
mnt_lf_files=()
survey_mnt_lf_files() {
    [ ! -d /mnt/lf ] && return 0
    debug "Surveying mnt lf"

    mapfile -t mnt_lf_files < <(find /mnt/lf -xdev -type f 2>/dev/null ||:)
    if [[ ${mnt_lf_files+x} = x ]]; then
        if (( ${#mnt_lf_files[@]} < 1 )); then
            totals[m]=0
            return
        fi
        totals[m]=$( du -xhc "${mnt_lf_files[@]}" 2>/dev/null | awk '/total/{print $1}' )
        [[ x${totals[m]} = x ]] && totals[m]=0 ||:
    else
        totals[m]=0
        return
    fi
    # set +vx
}

survey_dnf_cache() {
    local yum="dnf"
    which --skip-alias dnf &> /dev/null
    (( $? < 0 )) && yum="yum"
    debug "Surveying $yum cache"
    totals[n]=$(du -hc '/var/cache/{dnf,yum}' 2>/dev/null | awk '/total/{print $1}')
}

compressed_files=()
survey_compressed_files() {
    debug "Surveying compressed /home/lanforge "
    cd /home/lanforge
    mapfile -t compressed_files < <( find Documents/ html-reports/ lf_reports/ report-data/ tmp/ -type f \
        -a \( -name "*.gz" -o -name "*.xz" -o -name "*.bz2" -o -name "*.7z" -o -name "*.zip" \) 2>/dev/null ||:)
    if (( ${#compressed_files[@]} < 1 )); then
        debug "no compressed files found"
        totals[z]=0
        return
    fi

    totals[z]=$( du -xhc "${compressed_files[@]}" 2>/dev/null | awk '/total/{print $1}' )
    # set +veux
    [[ x${totals[z]} = x ]] && totals[z]=0 ||:
    cd -
}

## Find size of /lib/modules
# cd /lib/modules
# mapfile -t usage_libmod < <(du -sh *)

# Find how many kernels are installed
# cd /boot
# mapfile -t boot_kernels < <(ls init*)
# boot_usage=`du -sh .`

# report_files=()
survey_report_data() {
    debug "Surveying for lanforge report data"
    cd /home/lanforge

    local fsiz=0
    local fnum=0
    local csv_list=(`find report-data/ html-reports/ lf_reports/ -type f -a -name '*.csv' 2>/dev/null ||:`)
    local pdf_list=(`find report-data/ html-reports/ lf_reports/ Documents/ -type f -a -name '*.pdf' 2>/dev/null ||:`)
    local pcap_list=(`find tmp/ report-data/ local/tmp/ lf_reports/ Documents/ -type f -a \( -name '*.pcap' -o -name '*.pcapng' \) 2>/dev/null ||:`)
    fnum=$(( ${#csv_list[@]} + ${#pdf_list[@]} + ${#pcap_list[@]} ))

    if (( $fnum > 0 )); then
        fsiz=$(du -hc "${csv_list[@]}" "${pdf_list[@]}" "${pcap_list[@]}" | awk '/total/{print $1}')
    fi
    totals[r]="$fnum files ($fsiz): ${#csv_list[@]} csv, ${#pdf_list[@]} pdf, ${#pcap_list[@]} pcap"
    [[ x${totals[r]} = x ]] && totals[r]=0
    # report_files=("CSV files: $fnum tt $fsiz")
    cd "$starting_dir"
}


# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
#       gather usage areas
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
survey_areas() {
    local area
    note "Surveying..."
    for area in "${!surveyors_map[@]}"; do
        if (( $quiet < 1 )) && (( $verbose < 1 )); then
            echo -n "#"
        fi

        if [[ $area = b ]]; then
            if [[ ${kernel_sort_names+x} != x ]] || (( ${#kernel_sort_names[@] < 1 } )); then
                debug "surveying kernel area"
                # sleep 5
                ${surveyors_map[$area]}
            else
                debug "kernel area already surveyed"
            fi

        else
            debug "surveying $area"
            # sleep 2
            ${surveyors_map[$area]}
        fi
    done
    if (( $quiet < 1 )); then
        echo ""
    fi
}

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
#       report sizes here                                                 #
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
disk_usage_report() {
    for k in "${!totals[@]}"; do
        echo -e "\t${desc[$k]}:\t${totals[$k]}"
    done
}
survey_areas
disk_usage_report

if (( ${#core_files[@]} > 0 )); then
    hr
    note "${#core_files[@]} Core Files detected:"
    declare -A core_groups
    # set -e
    # note that the long pipe at the bottom of the loop is the best way to get
    # the system to operate with thousands of core files
    while read group7; do
        (( $verbose > 0 )) && echo -n '+'
        group7="${group7%, *}"
        group7="${group7//\'/}"
        [[ ${core_groups[$group7]+_} != _ ]] && core_groups[$group7]=0
        core_groups[$group7]=$(( ${core_groups[$group7]} + 1 ))
    done < <(echo "${core_files[@]}" | xargs file | awk -F": " '/execfn:/{print $7}')
    echo ""
    echo "These types of core files were found:"
    for group in "${!core_groups[@]}"; do
        echo "${core_groups[$group]} files of $group"
    done | sort -n
    hr
    (( ${#core_files[@]} > 0 )) && selections+=("c")
fi

#echo "Usage of /mnt: $usage_mnt"
#echo "Usage of /lib/modules: $usage_libmod"
#echo "Boot usage: $boot_usage"

#if (( ${#boot_kernels[@]} > 1 )); then
#    echo "Boot ramdisks:"
#    hr
#    printf '     %s\n' "${boot_kernels[@]}"
#    hr
#fi

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
#   delete extra things now                                               #
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

if contains "selections" "a" ; then
    # note "Automatic deletion will include: "
    # printf "%s\n" "${selections[@]}"
    debug "Doing automatic cleanup"
    for z in "${selections[@]}"; do
        debug "Will perform ${desc[$z]}"
        ${cleaners_map[$z]}
    done
    survey_areas
    disk_usage_report
    exit 0
fi

if (( ${#selections[@]} > 0 )) ; then
    debug "Doing selected cleanup: "
    # printf "    %s\n" "${selections[@]}"
    # sleep 1
    for z in "${selections[@]}"; do
        debug "Performing ${desc[$z]}"
        ${cleaners_map[$z]}
        # selections=("${selections[@]/$z}")
        remove selections "$z"
    done
    survey_areas
    disk_usage_report
else
    debug "No selections present"
fi

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
#   ask for things to remove if we are interactive                        #
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
choice=""
refresh=0
while [[ $choice != q ]]; do
    echo ""
    hr
    df -h --type ext4
    echo ""
    hr
    echo "What would you like to delete or compress? "
    echo "  b) old kernels                : ${totals[b]}"
    echo "  c) core crash files           : ${totals[c]}"
    echo "  d) old LANforge downloads     : ${totals[d]}"
    echo "  k) ath10k crash files         : ${totals[k]}"
    echo "  l) old /var/log files         : ${totals[l]}"
    echo "  m) orphaned /mnt/lf files     : ${totals[m]}"
    echo "  n) purge dnf/yum cache        : ${totals[n]}"
    echo "  r) report data                : ${totals[r]}"
    echo "  s) trash cans                 : ${totals[s]}"
    echo "  t) clean /var/tmp             : ${totals[t]}"
    echo "  z) list compressed files      : ${totals[z]}"
    echo "  q) quit"
    read -p "> " choice
    refresh=0
    case "$choice" in
    b )
        clean_old_kernels
        refresh=1
        ;;
    c )
        clean_core_files
        refresh=1
        ;;
    d )
        clean_lf_downloads
        refresh=1
        ;;
    k )
        clean_ath10_files
        refresh=1
        ;;
    l )
        clean_var_log
        refresh=1
        ;;
    m )
        clean_mnt_lf_files
        refresh=1
        ;;
    r )
        compress_report_data
        refresh=1
        ;;
    s )
        empty_trash_can
        refresh=1
        ;;
    t )
        clean_var_tmp
        refresh=1
        ;;
    z )
        clean_compressed_files
        refresh=1
        ;;
    q )
        echo ""
        exit
        ;;
    * )
        echo "not an option [$choice]"
        ;;
    esac
    if (( $refresh > 0 )) ; then
        survey_areas
        disk_usage_report
    fi
done
echo bye
