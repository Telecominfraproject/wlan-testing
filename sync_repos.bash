#!/bin/bash

# Copy wlan-lanforge-scripts into place
# Assumes wlan-lanforge-scripts is already up to date.
# Other setup may be added here as well.

if [ -d ../wlan-lanforge-scripts ]
then
    rm -fr lanforge/lanforge-scripts

    cp -a ../wlan-lanforge-scripts lanforge/lanforge-scripts
fi

