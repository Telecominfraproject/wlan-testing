#!/bin/bash

while true
do
      ../testbed_poll.pl --jfrog_passwd tip-read --jfrog_user tip-read --url http://orch/tip/testbeds/nola-basic-12/pending_work/ --dut_passwd openwifi --dut_user root
      sleep 120
done

