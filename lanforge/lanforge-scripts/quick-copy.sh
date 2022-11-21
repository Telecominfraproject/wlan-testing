#!/bin/bash

[[ x$1 == x ]] && echo "Copy to what hostname?" && exit 1
[ ! -f quick-copy.sh ] && echo "What directory are you in? $CWD" && exit 2

rm -f /tmp/qq.txt
find -iname "*pl" -o -iname "*pm" -o -iname "*sh" -o -iname "*py" > /tmp/qq.txt
rsync -rv --files-from=/tmp/qq.txt . "$1"
