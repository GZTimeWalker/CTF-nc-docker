#!/bin/sh

cd /home/ctf/files
nohup python3 -m http.server {download_port} > /var/log/file.log 2>&1 &

cd /
xinetd -dontfork
