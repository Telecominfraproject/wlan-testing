#!/bin/bash


if [ -d ../lanforge-scripts ]
then
    rm -fr lanforge/lanforge-scripts

    cp -a ../lanforge-scripts lanforge/lanforge-scripts
fi