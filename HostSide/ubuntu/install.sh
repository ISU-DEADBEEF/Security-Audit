#!/bin/bash

mkdir -p /usr/local/bin/audit

cp startConnection /usr/local/bin/audit/startConnection
cp file-sender.py /usr/local/bin/audit/file-sender.py

chmod +x /etc/init.d/audit /usr/local/bin/audit/file-sender.py

