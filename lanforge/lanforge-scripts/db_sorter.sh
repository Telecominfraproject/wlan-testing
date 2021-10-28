#!/bin/bash
#This script modifies DB directories so they appear alphabetically in LANforge.

# Script instructions
# First become root: su -
# Copy the script to /home/lanforge/scripts/
# cp db_sorter.sh /home/lanforge/scripts/
# Make the script executable:
# chmod +x /home/lanforge/scripts/db_sorter.sh
# Run script:
# /home/lanforge/scripts/db_sorter.sh

# If your databases are not in /home/lanforge/DB/ change the below line to reflect your DB directory's location.
db_dir="/home/lanforge/DB/"

# grab alphabetical list then use awk to just get dir name
# to sort reverse alphabetical order change ls -lr below to ls -l
dir_list=`ls -lr $db_dir | awk ' ''{print $9}' | grep -v "day_*"`

# goes through list, creates/removes file to trigger dir modified date
while read -r line; do
   if [[ $line != "" ]] && [[ -d ${db_dir}/${line} ]] && [[ $line != "day_*" ]]; then
      touch "${db_dir}/${line}/a"
      rm "${db_dir}/${line}/a"
   fi
   #needs sleep otherwise file mod date does not order correctly
   sleep .01s
done <<< "$dir_list"
