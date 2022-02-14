#!/bin/bash
# example based off https://www.endpoint.com/blog/2014/10/30/openssl-csr-with-alternative-names-one

hostname="$1"
hostname1=$hostname.local
ipaddr=

cat > tmp_csr_details.txt <<-EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = req_ext
distinguished_name = dn

[ dn ]
C=US
ST=Washington
L=Ferndale
O=Candela Technologies, Inc.
OU=LANforge
emailAddress=support@candelatech.com
CN = $hostname

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = $hostname1
DNS.2 = $ipaddr
EOF

# Let’s call openssl now by piping the newly created file in
openssl req -new -sha256 -nodes -out ${hostname}.csr -newkey rsa:2048\
 -keyout ${hostname}.key -config <( cat temp_csr_details.txt )
#
