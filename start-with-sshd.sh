#!/usr/bin/env bash

mkdir -p ~/.ssh
#env > ~/.ssh/environment

cp /root/container_ssh_key.priv /app/container_ssh_key.priv

tmux new -d -s sshd bash
tmux send-keys -t sshd '/usr/sbin/sshd -D' Enter

while [ 1 ] ; do
    sleep 100
done