#!/bin/bash

[ -z "$1" ] && echo "Please tell me where to place the files." && exit 1
[ ! -d "$1" ] && echo "I cannot see that directory." && exit 1
[ ! -w "$1" ] && echo "I cannot write to that directory." && exit 1

sizes=( 4K 48K 128K 256K 2048K )
name_prefix="data_slug"
index="$1/slug_list.html"
cat > $index <<EOF
<html><head>
<title>Files of random data</title>
</head>
<body>
<h1>Files of random data</h1>
<ul>
EOF
for s in "${sizes[@]}"; do
   fname="${name_prefix}_${s}.bin"
   echo "<li><a href='$fname'>$fname</a></li>" >> $index
   dd if=/dev/urandom of="$1/$fname" iflag=fullblock oflag=direct bs=${s} count=1
done
echo "</ul></html>" >> $index
ls -lSs $1/$name_prefix*
#
