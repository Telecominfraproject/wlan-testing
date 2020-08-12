#!/bin/bash

while true
do
      ../testbed_poll.pl --jfrog_passwd tip-read --jfrog_user tip-read --url http://orch/tip/testbeds/nola-basic-01/pending_work/
      sleep 120
done

