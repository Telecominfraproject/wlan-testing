#!/bin/bash

while true
do
      ../testbed_poll.pl --jfrog_passwd tip-read --jfrog_user tip-read --url http://orch/tip/testbeds/ferndale-basic-01/pending_work/
      exit 0
done
