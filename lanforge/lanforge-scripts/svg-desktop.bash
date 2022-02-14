#!/bin/bash
Q='"'
A="'"
function set_background() {
   gsettings set "org.mate.background" "$1" "$2"
}

SourceFile="/usr/share/backgrounds/mate/desktop/Ubuntu-Mate-Cold-no-logo.png"
DesktopFile="/home/lanforge/Pictures/desktop.svg"
my_version=`cat /var/www/html/installed-ver.txt`
my_hostname=`hostname`
my_dev=`ip ro sho | awk '/default via/{print $5}'`
my_ip=`ip a sho $my_dev | awk '/inet /{print $2}'`
my_mac=`ip a sho | grep -A1 "$my_dev" | awk '/ether /{print $2}'`
fill_color=${my_mac//:/}
fill_color=${fill_color:6:12}
X=220
Y=150
#convert -pointsize 80 -fill "#$fill_color" -stroke black -strokewidth 1 \
#  -draw "text $X,$Y \"$my_hostname\"" \
#  -draw "text $X,$(( Y + 75 )) \"$my_dev $my_ip\"" \
#  -draw "text $X,$(( Y + 150 )) \"$my_mac\"" \
#  $SourceFile \
#  -scale 1600x900 \
#  $DesktopFile

cat > $DesktopFile <<_EOF_
<svg viewBox='0 0 1600 900' width='1600' height='900' xmlns='http://www.w3.org/2000/svg'>
<style>
text {
    fill: #$fill_color;
    stroke: black;
    text-anchor: left;
    font-size: 35px;
    font-family: 'DejaVu Sans Bold', sans-serif;
    font-weight: bold;
    opacity: 0.8;
}
#bgrec {
    fill: gray;
    opacity: 0.5;
    stroke-width: 8px;
    stroke: rgba(50, 50, 50, 255);
}
</style>
<g>
    <rect id='bgrec' x='150' y='30' rx='10' ry='10' width='550px' height='160px'></rect>
    <g>
        <text x='170' y='70'>$my_hostname</text>
        <text x='170' y='120'>$my_dev $my_ip</text>
        <text x='170' y='170'>$my_mac</text>
    </g>
</g>
</svg>
_EOF_


set_background picture-filename ${A}${DesktopFile}${A}
set_background picture-options  'stretched'
#
