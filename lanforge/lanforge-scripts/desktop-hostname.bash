#!/bin/bash
Q='"'
A="'"
function set_background() {
   gsettings set "org.mate.background" "$1" "$2"
}

SourceFile="/usr/share/backgrounds/mate/desktop/Ubuntu-Mate-Cold-no-logo.png"
DesktopFile="/home/lanforge/desktop.png"
my_hostname=`hostname`
my_os="[os]"
if [ -f /etc/os-release ]; then
    my_os=`egrep '^VERSION=' /etc/os-release`
    if [ ! -z "$my_os" ]; then
        my_os="${my_os/VERSION=/}"
        my_os="${my_os//\"/}"
    fi
fi

my_inver="[lfver]"
if [ -f "/var/www/html/installed-ver.txt" ]; then
    my_inver=`cat /var/www/html/installed-ver.txt`;
fi
my_kver=`uname -r`
my_dev=`ip ro sho | awk '/default via/{print $5}'`
my_ip=`ip a sho $my_dev | awk '/inet /{print $2}'`
my_mac=`ip a sho | grep -A1 "$my_dev" | awk '/ether /{print $2}'`
fill_color=${my_mac//:/}
fill_color=${fill_color:6:12}
X=220
Y=150
convert -pointsize 80 -fill "#$fill_color" -stroke black -strokewidth 1 \
  -draw "text $X,$Y \"$my_hostname\"" \
  -draw "text $X,$(( Y + 75 )) \"LANForge $my_inver\"" \
  -draw "text $X,$(( Y + 155 )) \"Kernel $my_kver $my_os\"" \
  -draw "text $X,$(( Y + 225 )) \"$my_dev $my_ip\"" \
  -draw "text $X,$(( Y + 295 )) \"$my_mac\"" \
  $SourceFile \
  -scale 1600x900 \
  $DesktopFile

set_background picture-filename ${A}${DesktopFile}${A}
set_background picture-options  'stretched'
#
