#!/bin/bash

while true
do
	../testbed_poll.pl --jfrog_passwd tip-read --jfrog_user tip-read --url http://192.168.100.195/tip/testbeds/ben-home-ecw5410/pending_work/ || exit 1
	sleep 120
done

