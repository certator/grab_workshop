#!/usr/bin/env bash

source ./.env

PLATFORM=unknown

if cat /etc/os-release 2>&1| grep ubuntu > /dev/null 2>&1 && which ifconfig > /dev/null; then
    PLATFORM=ubuntu
fi

if [ $(uname -s) == Darwin ]; then
    PLATFORM=osx
fi

echo "current platform" $PLATFORM

if [ $PLATFORM == unknown ]; then
    echo 'can not detect platform'
    exit 1
fi

if [ $PLATFORM == ubuntu ]; then
    sudo ifconfig lo:0 $DEV_LOOPBACK_IP up
fi

if [ $PLATFORM == osx ]; then
    sudo ifconfig lo0 alias $DEV_LOOPBACK_IP
fi

if ping -c 1 -i 1 -W 1 $DEV_LOOPBACK_IP > /dev/null ; then
    echo 'dev IP' $DEV_LOOPBACK_IP 'has been set up successfully'
else
    echo 'dev IP was not created'
    exit 1
fi
