#!/bin/bash

echo "===== SYSTEM INFORMATION ====="
echo "Hostname: $(hostname)"
echo "OS:"
cat /etc/os-release | head -5
echo
echo "Kernel:"
uname -r
echo
echo "CPU:"
nproc
echo
echo "Memory:"
free -h
echo
echo "Disk:"
df -h /
