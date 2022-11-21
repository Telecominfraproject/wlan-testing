#!/bin/bash
Q='"'
A="'"
function set_background() {
   gsettings set "org.mate.background" "$1" "$2"
}
. /etc/os-release
SourceFile="/usr/share/backgrounds/mate/desktop/Ubuntu-Mate-Cold-no-logo.png"
DesktopFile="/home/lanforge/Pictures/desktop.svg"
my_version=`cat /var/www/html/installed-ver.txt`
my_hostname=`hostname`
my_dev=`ip ro sho | awk '/default via/{print $5}'`
my_ip=`ip a sho $my_dev | awk '/inet /{print $2}'`
my_mac=`ip a sho | grep -A1 "$my_dev" | awk '/ether /{print $2}'`
my_os="$PRETTY_NAME"
my_realm=`awk '/^realm / {print $2}' /home/lanforge/config.values`
my_resource=`awk '/^first_client / {print $2}' /home/lanforge/config.values`
my_mode=`awk '/^mode / {print $2}' /home/lanforge/config.values`
my_lfver=`cat /var/www/html/installed-ver.txt`
fill_color=${my_mac//:/}
fill_color=${fill_color:6:12}
X=220
Y=150

if (( $my_realm == 255 )); then
    my_realm="Stand Alone"
else
    my_realm="Realm $my_realm"
fi
#convert -pointsize 80 -fill "#$fill_color" -stroke black -strokewidth 1 \
#  -draw "text $X,$Y \"$my_hostname\"" \
#  -draw "text $X,$(( Y + 75 )) \"$my_dev $my_ip\"" \
#  -draw "text $X,$(( Y + 150 )) \"$my_mac\"" \
#  $SourceFile \
#  -scale 1600x900 \
#  $DesktopFile

#    font-family: 'Source Code Pro', 'FreeMono', 'Liberation Mono', 'DejaVu Sans Mono', 'Lucida Sans Typewriter', 'Consolas',  mono, sans-serif;

imgtag=""
ANV="/home/lanforge/Pictures/anvil-right.svg"
if [ -r "$ANV" ] ; then
    imgtag="<image x='400' y='200' width='800' height='450' href='$ANV' />"
fi

cat > $DesktopFile <<_EOF_
<svg viewBox='0 0 1600 900' width='1600' height='900' xmlns='http://www.w3.org/2000/svg'>
<style>
text {
    fill: #$fill_color;
    stroke: rgba(4, 64, 4, 64);
    stroke-width: 1px;
    text-anchor: left;
    font-size: 36px;
    font-family: 'Consolas';
    font-weight: bold;
    opacity: 0.8;
}
#bgrec {
    fill: gray;
    opacity: 0.5;
    stroke-width: 6px;
    stroke: rgba(50, 50, 50, 255);
}
</style>
<g>
    <rect id='bgrec' x='260' y='50' rx='10' ry='10' width='600px' height='210px'>
    </rect>
    <g>
        <text x='270' y='85'>$my_hostname LANforge $my_lfver</text>
        <text x='270' y='125'>$my_realm Resource 1.$my_resource</text>
        <text x='270' y='165'>$my_dev $my_ip</text>
        <text x='270' y='245'>$my_mac</text>
        <text x='270' y='205'>$my_os</text>
    </g>
</g>
$imgtag
</svg>
_EOF_
set_background picture-filename ${A}${DesktopFile}${A}
set_background picture-options  'stretched'
#
