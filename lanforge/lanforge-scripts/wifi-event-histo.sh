#!/bin/bash
set +x
if [[ x"$1" = x ]]; then
   echo "want a filename, bye"
   exit 1
fi
echo -n "* WIFI-connection events: "
grep 'connected to' "$1" | sort | uniq | wc -l

echo -n "* Wifi auth events: "
grep ' auth .* status: 0' "$1" | sort | uniq | wc -l

echo -n "* Roaming attempt before association: {too_early}: "
grep '{too_early}' "$1" | sort | uniq | wc -l

echo -n "* DHCP Failure: "
grep 'DHCP Failure' "$1" | sort | uniq |  wc -l

echo -n "* Skipped Roam-to-Self events: "
fgrep 'already associated with AP' "$1" | sort | uniq |  wc -l

echo -n "* Roam verify failure: "
grep 'WARNING:  Requested' "$1" | sort | uniq |  wc -l

echo -n "* Not associated:"
grep 'Not-Associated' "$1" | sort | uniq |  wc -l

echo -n "* Link Down: "
grep 'Link DOWN' "$1" | sort | uniq |  wc -l

echo -n "* Link Up: "
grep 'Link UP' "$1" | sort | uniq |  wc -l

echo -n "* first_page_load: "
grep 'first_page_load' "$1" | sort | uniq | wc -l

echo -n "* saw_http_redirect: "
grep 'saw_http_redirect' "$1" | sort | uniq | wc -l

echo -n "* find_redirect_url: "
grep  find_redirect_url "$1" | sort | uniq | wc -l

echo -n "* request meta redirect: "
grep  "request meta redirect" "$1" | sort | uniq | wc -l

echo -n "* redirect_response: "
grep redirect_response "$1" | sort | uniq | wc -l

echo -n "* submitting .*guest: "
grep 'submitting .*guest' "$1" | sort | uniq | wc -l

echo -n "* response from .*guest: "
grep 'response from .*guest' "$1" | sort | uniq | wc -l

echo -n "* submitting .*securelogin: "
grep 'submitting .*securelogin' "$1" | sort | uniq | wc -l

echo -n "* response from .*securelogin: "
grep 'response from .*securelogin' "$1" | sort | uniq | wc -l

echo -n "* portal_login: OK -LOGIN: "
grep 'portal_login: OK -LOGIN' "$1" | sort | uniq | wc -l

echo -n "* missing_redirect: "
grep missing_redirect "$1" | sort | uniq | wc -l

echo -n "* submit_start_url did not see redirect: "
grep 'submit_start_url did not see redirect' "$1" | sort | uniq | wc -l

#
