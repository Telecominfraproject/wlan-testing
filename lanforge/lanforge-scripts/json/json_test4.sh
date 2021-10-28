#!/bin/bash
set -e
unset proxy
unset http_proxy
Q='"'
q="'"
S='*'
application_json="application/json"
accept_json="Accept: $application_json"
accept_html='Accept: text/html'
accept_text='Accept: text/plain'
#accept_any="'Accept: */*'" # just dont use
content_plain='Content-Type: text/plain'
content_json="Content-Type: $application_json"
switches='-sqv'
#switches='-sq'
data_file=/var/tmp/data.$$

function Kurl() {
   echo "======================================================================================="
   echo "curl $switches $@"
   echo "======================================================================================="
   curl $switches "$@" | json_pp
   echo ""
   echo "======================================================================================="
}

function Jurl() {
   echo "=J====================================================================================="
   echo "curl $switches -H $accept_json -H $content_json $@"
   echo "=J====================================================================================="
   curl $switches -H "$accept_json" -H "$content_json" -X POST "$@"
   echo ""
   echo "=J====================================================================================="
}

#url="http://jed-f24m64-9119:8080"
url="http://127.0.0.1:8080"
while true; do
   curl -sq -H "$accept_html" $url/help/ > /var/tmp/help.html
   perl -ne "m{href='(/help/[^']+)'} && print \"\$1\n\";" /var/tmp/help.html > /var/tmp/help_cmds.txt
   for f in `cat /var/tmp/help_cmds.txt`; do
      curl --retry 10 -sq -H "$accept_html" "${url}$f" >/dev/null
   done

   curl -sq -H "$accept_json" ${url}/resource/list | json_reformat > $data_file
#less $data_file
   perl -ne 'm{"_links"\s*:\s*"([^ ]+)"} && print "$1\n";' $data_file > /var/tmp/resources.txt

   for f in `cat /var/tmp/resources.txt`; do
      echo "$f"
      (curl  --retry 10 -sq -H "$accept_json" "${url}$f" |json_reformat) || exit 1
   done

   curl -sq -H "$accept_json" ${url}/port/list | json_reformat > $data_file
#less $data_file
   perl -ne 'm{"_links"\s*:\s*"([^ ]+)"} && print "$1\n";' $data_file > /var/tmp/ports.txt

   for f in `cat /var/tmp/ports.txt`; do
      echo "$f"
      (curl  --retry 10 -sq -H "$accept_json" "${url}$f" |json_reformat) || exit 1
   done
done

#
