#!/bin/bash
# Setup python environment variable and pip environment variable like
# export PYTHON=/usr/bin/python3
# export PIP=/usr/bin/pip3
#sh setup_env.bash -t tip_2x -d all -n "Shivam Thakur" -o TIP -e shivam.thakur@candelatech.com -i "TIP OpenWIFI 2.X Library"
helpFunction()
{
   echo "Open Wifi CICD Test Automation Installation"
   echo "Usage: $0 -t target -d device "
   echo -e "\t-t Target SDK (AP and/or controller Library) eg. tip_2x"
   echo -e "\t-n Author Name eg. Shivam Thakur"
   echo -e "\t-o Organization eg. tip_2x"
   echo -e "\t-e Author Email Address eg. tip_2x"
   echo -e "\t-i Description Info eg. tip_2x"
   echo -e "\t-d Test Device Name eg. lanforge | perfecto | all"
   exit 1 # Exit script after printing help
}

while getopts "t:n:o:e:i:d:" opt
do
   case "$opt" in
      t ) target="$OPTARG" ;;
      n ) author="$OPTARG" ;;
      o ) org="$OPTARG" ;;
      e ) email="$OPTARG" ;;
      i ) description="$OPTARG" ;;
      d ) device="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$target" ] || [ -z "$author" ] || [ -z "$org" ] || [ -z "$email" ] || [ -z "$description" ] || [ -z "$device" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

# Begin script in case all parameters are correct
echo "Target SDK for " "$target"
echo "$device"

# Check Python version and pip version
if ! hash $PYTHON; then
    echo "python is not installed"
    exit 1
fi

ver=$($PYTHON -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
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
    cd wlan-lanforge-scripts
    git checkout WIFI-1321-create-a-lan-forge-pip-module
    cd ../wlan-testing/
  fi
  if [ -d ../wlan-lanforge-scripts ]
  then
    cd ../wlan-lanforge-scripts
    rm -rf ../lanforge_scripts
    sh to_pip.sh
    pip install ../lanforge_scripts/dist/*.whl #--force-reinstall
    echo "Installed LANforge PIP Module"
    cd ../wlan-testing/
    rm tests/imports.py
    touch tests/imports.py
    if [ $target == "tip_2x" ]
    then
      cd libs/tip_2x
      python setup.py bdist_wheel
      pip install dist/*.whl --force-reinstall
      cd ../../
    fi
    echo -e "\"\"\"\nRegistered Target Imports\n\"\"\"\nimport sys\nimport importlib\n\nsys.path.append('/usr/local/bin')\n\n" >> tests/imports.py
    echo -e "########################################################################################################################" >> tests/imports.py
    echo -e "\"\"\"
    Target Name:$target
    Author Name:$author
    Organization:$org
    Register ID:1
    Email:$email
    description:$description
\"\"\"" >> tests/imports.py
  echo -e "
try:
    target = importlib.import_module(\"tip_2x\")
    target = target.tip_2x
except ImportError as e:
    print(e)
    sys.exit(\"Python Import Error: \" + str(e))
" >> tests/imports.py
    echo -e "########################################################################################################################" >> tests/imports.py
    echo -e "########################################################################################################################" >> tests/imports.py
    echo -e "\"\"\"
    Target Name:lanforge_scripts
    Author Name:$author
    Organization:$org
    Register ID:2
    Email:$email
    description:Candela LANforge Based Library
\"\"\"" >> tests/imports.py
  echo -e "
try:
    lanforge_libs = importlib.import_module(\"lanforge_scripts.lf_libs.lf_libs\")
    lf_libs = lanforge_libs.lf_libs
    lanforge_tests = importlib.import_module(\"lanforge_scripts.lf_libs.lf_tests\")
    lf_tests = lanforge_tests.lf_tests
except ImportError as e:
    print(e)
    sys.exit(\"Python Import Error: \" + str(e))
" >> tests/imports.py
   echo -e "########################################################################################################################" >> tests/imports.py
    # TODO Create a perfecto pip module baseline method
  fi
fi
