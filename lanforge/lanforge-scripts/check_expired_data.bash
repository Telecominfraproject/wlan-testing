#!/bin/bash
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
#  check_expired_data.bash                                          #
#                                                                   #
#  Use this script to find and remove reports older than the        #
#  specified number of days. Please use with caution.               #
#                                                                   #
#  You can install this as a cron job by making a wrapper script    #
#  and placting the wrapper script in /etc/cron.daily               #
#                                                                   #
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
#set -veux
usage="
-d <directory> Find data within this directory (required)
-t <days>   Find data this many days old or older (required)
-f          Delete files (not a default option)
-v          Print files

See the files you would delete:
$0 -d /home/lanforge/report-data -t 11 -v

Actually delete the files:
$0 -d /home/lanforge/report-data -t 11 -f

You may create a script in /etc/cron.daily like this:
 ----- ----- ----- ----- ----- ----- ----- ----- -----
#!/bin/bash
LF='/home/lanforge'
E='/home/lanforge/scripts/check_expired_data.bash'
$E -d \$LF/report-data -t 11 -f
$E -d \$LF/html-reports -t 11 -f
 ----- ----- ----- ----- ----- ----- ----- ----- -----
"

if (( $# < 2 )); then
    echo "$usage"
    exit 1
fi

actually_delete=0
data_dir=""
days_old=0 # zero will mean don't do anything
verbose=0
while getopts "d:ht:fv" arg; do
    case $arg in
        h)
            echo "$usage"
            exit 0
            ;;
        d)
            if [[ x$OPTARG = x ]]; then
                echo "data dir required"
                exit 1
            fi
            data_dir="$OPTARG"
            ;;
        f)
            actually_delete=1
            ;;
        t)
            if [[ x$OPTARG = x ]] || (( $OPTARG < 1 )); then
                echo "time in days required, one or more days"
                exit 1
            fi
            days_old="$OPTARG"
            ;;
        v)
            verbose=1
            ;;
        *)
            echo "Unkown option $arg"
            exit 1
    esac
done

if [[ ! -d $data_dir ]]; then
    echo "Directory not found: $data_dir"
    exit 1
fi
#set -veux
files_list=()
mapfile -d '' files_list < <(find  -L "$data_dir" -type f -mtime +$days_old -print0)

if (( "${#files_list[@]}" < 1 )); then
    echo "No files found"
    exit 0
fi
echo "Found $((${#files_list[@]} + 1 )) files"
if (( $verbose == 1 )) ; then
    printf "%s\n" "${files_list[@]}" | xargs -n 3 echo
fi


if (( $actually_delete == 1 )); then
    echo -n "Deleting files..."
    printf "%s\n" "${files_list[@]}" | xargs rm
    echo "done"
else
    echo "Not deleting files."
fi
