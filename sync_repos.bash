#!/bin/bash

# Copy wlan-lanforge-scripts into place
# Assumes wlan-lanforge-scripts is already up to date.
# Other setup may be added here as well.

if [ -d ../wlan-lanforge-scripts ]
then
    rm -fr libs/lanforge/lanforge-scripts

    cp -ar ../wlan-lanforge-scripts libs/lanforge/lanforge-scripts
fi
if [ -d tests/logs ]
then
  rm -fr tests/logs
  mkdir tests/logs
fi
if [ -d tests/reports ]
then
  rm -fr tests/reports
  mkdir tests/reports
fi