#!/bin/bash

echo "===== SERVER HEALTH CHECK ====="
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo

echo "--- Uptime ---"
uptime
echo

echo "--- Memory ---"
free -h
echo

echo "--- Disk ---"
df -h /
echo

echo "--- Network ---"
ping -c 1 8.8.8.8 >/dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Network: ONLINE"
else
    echo "Network: OFFLINE"
fi

echo "=============================="
