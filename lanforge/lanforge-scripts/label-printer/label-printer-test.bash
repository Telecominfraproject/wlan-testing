#!/bin/bash

#printer="LabelWriter-450"
printer="QL-800"

curl -v -d "printer=${printer}&model=lf0350&mac=00:0e:84:33:44:55:66&hostname=vm-atlas20&serial=zoso1234" http://localhost:8082/
sleep 4
curl -v -d "printer=${printer}&model=lf0350&mac=00:0e:84:33:44:55:66&hostname=&serial=" http://localhost:8082/
sleep 4
curl -v -d "printer=${printer}&model=lf0350&mac=00:0e:84:33:44:55:66"  http://localhost:8082/
