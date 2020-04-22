# Example test-bed configuration

# Scripts should source this file to set the default environment variables
# and then override the variables specific to their test case (and it can be done
# in opposite order for same results
#
# After the env variables are set,
# call the 'lanforge/lanforge-scripts/gui/basic_regression.bash'
# from the directory in which it resides.

PWD=`pwd`
AP_AUTO_CFG_FILE=${AP_AUTO_CFG_FILE:-$PWD/AP-Auto-ap-auto-228.txt}
WCT_CFG_FILE=${WCT_CFG_FILE:-$PWD/WCT-228sta.txt}
DPT_CFG_FILE=${DPT_CFG_FILE:-$PWD/dpt-pkt-sz.txt}
SCENARIO_CFG_FILE=${SCENARIO_CFG_FILE:-$PWD/228_sta_scenario.txt}

# LANforge target machine
LFMANAGER=${LFMANAGER:-192.168.3.190}

# LANforge GUI machine (may often be same as target)
GMANAGER=${GMANAGER:-192.168.3.190}
GMPORT=${GMPORT:-3990}
MY_TMPDIR=${MY_TMPDIR:-/tmp}

# Test configuration (10 minutes by default, in interest of time)
STABILITY_DURATION=${STABILITY_DURATION:-600}
TEST_RIG_ID=${TEST_RIG_ID:-Ben-Home-OTA}

# DUT configuration
DUT_FLAGS=${DUT_FLAGS:-22}  # AP, WPA-PSK
DUT_FLAGS_MASK=${DUT_FLAGS_MASK:-0xFFFF}
DUT_SW_VER=${DUT_SW_VER:-OpenWrt-Stock}
DUT_HW_VER=Linksys-MR8300
DUT_MODEL=Linksys-MR8300
DUT_SERIAL=${DUT_SERIAL:-NA}
DUT_SSID1=${DUT_SSID1:-Connectus-local}
DUT_SSID2=${DUT_SSID2:-Connectus-local-5}
DUT_SSID3=${DUT_SSID3:-Connectus-local-5}
DUT_PASSWD1=${DUT_PASSWD1:-12345678}
DUT_PASSWD2=${DUT_PASSWD2:-12345678}
DUT_PASSWD3=${DUT_PASSWD3:-12345678}
DUT_BSSID1=32:23:03:81:9c:29
DUT_BSSID2=30:23:03:81:9c:27
DUT_BSSID3=30:23:03:81:9c:28

export AP_AUTO_CFG_FILE WCT_CFG_FILE DPT_CFG_FILE SCENARIO_CFG_FILE
export LFMANAGER GMANAGER GMPORT MY_TMPDIR
export STABILITY_DURATION TEST_RIG_ID
export DUT_FLAGS DUT_FLAGS_MASK DUT_SW_VER DUT_HW_VER DUT_MODEL
export DUT_SERIAL DUT_SSID1 DUT_SSID2 DUT_SSID3
export DUT_PASSWD1 DUT_PASSWD2 DUT_PASSWD3
export DUT_BSSID1 DUT_BSSID2 DUT_BSSID3

