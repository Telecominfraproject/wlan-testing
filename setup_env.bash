#!/bin/bash

helpFunction()
{
   echo "Open Wifi CICD Test Automation Installation"
   echo "Usage: $0 -t target -d device "
   echo -e "\t-t|--target Target SDK (AP and/or controller Library) eg. tip_2x"
   echo -e "\t-d|--device Test Device Name eg. lanforge | perfecto | all"
   exit 1 # Exit script after printing help
}

while getopts "t:d:" opt
do
   case "$opt" in
      t ) target="$OPTARG" ;;
      d ) device="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$target" ] || [ -z "$device" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

# Begin script in case all parameters are correct
echo "Target SDK for " "$target"
echo "$device"

# Check Python version and pip version
if ! hash python; then
    echo "python is not installed"
    exit 1
fi

ver=$(python -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" -lt "38" ]; then
    echo "This script requires python 3.8 or greater"
    exit 1
fi

if  [ "$device" == "lanforge" ] || [ "$device" == "all" ]
then
   if [ ! -d ../wlan-lanforge-scripts ]
  then
    cd ..
    git clone https://github.com/Telecominfraproject/wlan-lanforge-scripts
    cd wlan-testing/
  fi
  if [ -d ../wlan-lanforge-scripts ]
  then
    cd ../wlan-lanforge-scripts
    rm -rf ../lanforge_scripts
    sh to_pip.sh
    pip install ../lanforge_scripts/dist/*.whl #--force-reinstall
    echo "Installed LANforge PIP Module"
    cd ../wlan-testing
    # TODO Create a imports.py in tests directory for getting necessary imports which are nothing but dynamic imports,
    #  Also, install the necessary requirements.txt file and check the pytest command line argument
    #  Also, install java and allure command line tool
  fi
fi
