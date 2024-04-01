#!/bin/bash

mkdir -p /usr/local/bin/audit
mkdir -p /etc/init.d/audit

cp startConnection /etc/init.d/audit/startConnection
cp file-sender.py /usr/local/bin/audit/file-sender.py

chmod +x /etc/init.d/audit /usr/local/bin/audit/file-sender.py
