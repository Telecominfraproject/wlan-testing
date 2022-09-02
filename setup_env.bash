#!/usr/bin/bash
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
x=$($PYTHON -V)
echo $x
ver=$([[ "$x" =~ "Python 3" ]] && echo "38")
echo $ver
#ver=$($PYTHON -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
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
    $PIP uninstall ../lanforge_scripts/dist/*.whl
    rm -rf ../lanforge_scripts
    bash to_pip.sh
    $PIP install ../lanforge_scripts/dist/*.whl #--force-reinstall
    echo "Installed LANforge PIP Module"
    cd ../wlan-testing/
    mkdir ~/.pip
    echo "[global]" > ~/.pip/pip.conf
    echo "index-url = https://pypi.org/simple" >> ~/.pip/pip.conf
    echo "extra-index-url = https://tip-read:tip-read@tip.jfrog.io/artifactory/api/pypi/tip-wlan-python-pypi-local/simple" >> ~/.pip/pip.conf
    $PIP install -r requirements.txt
    rm tests/imports.py
    touch tests/imports.py
    if [ $target == "tip_2x" ]
    then
      cd libs/tip_2x
      $PYTHON setup.py bdist_wheel
      $PIP install dist/*.whl --force-reinstall
      cd ../../
    fi
    x=$(whoami)
    echo -e "\"\"\"\nRegistered Target Imports\n\"\"\"\nimport sys\nimport importlib\n\nsys.path.append('/usr/local/bin')\n\nsys.path.append('/home/$x/.local//bin/')\n\nsys.path.append('/home/$x/.local/lib/python3.8/site-packages/')\n\n" >> tests/imports.py
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
    scp_file = lanforge_libs.SCP_File
    lanforge_tests = importlib.import_module(\"lanforge_scripts.lf_libs.lf_tests\")
    lf_tests = lanforge_tests.lf_tests
except ImportError as e:
    print(e)
    sys.exit(\"Python Import Error: \" + str(e))
" >> tests/imports.py
   echo -e "########################################################################################################################" >> tests/imports.py
    cd libs/perfecto_interop
    $PYTHON setup.py bdist_wheel
    $PIP install dist/*.whl --force-reinstall
    cd ../../
    echo -e "########################################################################################################################" >> tests/imports.py
    echo -e "\"\"\"
    Target Name:perfecto_interop
    Author Name:$author
    Organization:$org
    Register ID:2
    Email:$email
    description:Perfecto Based Interop Library
\"\"\"" >> tests/imports.py
  echo -e "
try:
    perfecto_interop = importlib.import_module(\"perfecto_interop\")
    android_tests = perfecto_interop.android_tests
    ios_tests = perfecto_interop.ios_tests
except ImportError as e:
    print(e)
    sys.exit(\"Python Import Error: \" + str(e))
" >> tests/imports.py
   echo -e "########################################################################################################################" >> tests/imports.py


  fi
fi
WLAN_TESTING_PATH=$(pwd)"/tests/"
echo $WLAN_TESTING_PATH
rm tests/pytest.ini
touch tests/pytest.ini
echo -e "[pytest]
python_files = test_*.py setup_*.py
norecursedirs = .svn _build tmp*
addopts= --junitxml=test_everything.xml
log_format = %(asctime)s %(levelname)s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S
;norecursedirs=out build
num_stations=1
testpaths =
     $WLAN_TESTING_PATH

# Cloud SDK settings
sdk-customer-id=2

#fIRMWARE Option
firmware=0

# Radius Settings
radius_server_ip=192.168.200.75
radius_port=1812
radius_secret=testing123


# Testrail Info
tr_url=https://telecominfraproject.testrail.com
tr_user=cicd@tip.com
tr_pass=Open$Wifi123
tr_project_id=WLAN
tr_prefix=TIP_
milestone=29



filterwarnings=ignore::UserWarning


markers =
    ;   Test Suites, It Contains
    ow_sanity_lf: OpenWifi Sanity Test Plan
    ow_performance_lf: OpenWifi Performance Test Plan
    ow_sanity_interop: OpenWifi Sanity with Interop

    ;   Test Suites, It Contains
    client_connectivity_tests: Client Connectivity Test Cases with bridge|nat|vlan modes across 2.4|5|6 GHz bands with Various Encryptions
    dfs_tests: Dynamic Frequency Selection Test Cases
    multi_psk_tests: Multi PSK Test Cases
    rate_limiting_tests: Rate Limiting Test Cases
    dvlan_tests: Dynamic VLAN Test Cases
    dynamic_qos_tests: Dynamic QOS Test Cases
    multi_vlan_tests: Multi VLAN Combination based Test Cases

    client_scale_tests: Client Capacity Tests with maximum possible Stations bridge|nat|vlan 2.4|5|6 GHz Bands
    peak_throughput_tests: Single Client Peak Performance Test with various Bandwidths across 2.4|5|6 GHz Bands with various Client Types
    dataplane_tests: Single Client Throughput Test with various pkt sizes with UL|DL|BI with AC|AX Client Types across 2.4|5|6 GHz Bands
    multi_band_tests: Multi Band Performance Test on bridge|nat|vlan mode with Single Client on each of the 2.4|5|6 GHz Bands

    rate_vs_range_tests: Rate verses Range Tests with Various Combinations bridge|nat|vlan 2.4|5|6 GHz Bands
    rate_vs_orientation_tests: Rate verses Orientation Tests with Various Combinations bridge|nat|vlan 2.4|5|6 GHz Bands
    rx_sensitivity_tests: Receiver Sensitivity Tests with Various Combinations bridge|nat|vlan 2.4|5|6 GHz Bands
    spatial_consistency_tests: Spatial Consistency Tests with Various Combinations bridge|nat|vlan 2.4|5|6 GHz Bands
    multi_assoc_disassoc_tests: Multi Association and Disassociation Tests with Various Combinations bridge|nat|vlan 2.4|5|6 GHz Bands
    multi_station_performance_tests: Multi Station Performance Tests with Various Combinations bridge|nat|vlan 2.4|5|6 GHz Bands
    mu_mimo_performance_tests: Multi User MIMO Tests with Various Combinations bridge|nat|vlan 2.4|5|6 GHz Bands
    ofdma_tests: OFDMA Tests with Various Combinations bridge|nat|vlan 2.4|5|6 GHz Bands


    ;   Supported Markers
    bridge: Use this marker to run bridge mode tests in each of the above test plans/suites
    nat: Use this marker to run nat mode tests in each of the above test plans/suites
    vlan: Use this marker to run vlan mode tests in each of the above test plans/suites

    twog: Use this marker to run 2.4 GHz tests in each of the above test plans/suites
    fiveg: Use this marker to run 5 GHz tests in each of the above test plans/suites
    sixg: Use this marker to run 6 GHz tests in each of the above test plans/suites

    open: Use this marker to run open Encryption tests in each of the above test plans/suites
    wpa: Use this marker to run wpa Encryption tests in each of the above test plans/suites
    wpa2_personal: Use this marker to run wpa2_personal Encryption tests in each of the above test plans/suites
    wpa3_personal: Use this marker to run wpa3_personal Encryption tests in each of the above test plans/suites
    wpa3_personal_mixed: Use this marker to run wpa3_personal_mixed Encryption tests in each of the above test plans/suites
    wpa_wpa2_personal_mixed: Use this marker to run wpa_wpa2_personal_mixed Encryption tests in each of the above test plans/suites

    wpa_enterprise: Use this marker to run wpa_enterprise Encryption tests in each of the above test plans/suites
    wpa2_enterprise: Use this marker to run wpa2_enterprise Encryption tests in each of the above test plans/suites
    wpa3_enterprise: Use this marker to run wpa3_enterprise Encryption tests in each of the above test plans/suites
    wpa_wpa2_enterprise_mixed: Use this marker to run wpa_wpa2_enterprise_mixed Encryption tests in each of the above test plans/suites
    wpa3_enterprise_mixed: Use this marker to run wpa3_enterprise_mixed Encryption tests in each of the above test plans/suites
" >> tests/pytest.ini

