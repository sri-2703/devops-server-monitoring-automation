#!/bin/bash

SOURCE="logs"
BACKUP_DIR="backups"

mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE="$BACKUP_DIR/logs_$TIMESTAMP.tar.gz"

tar -czf "$ARCHIVE" "$SOURCE"

echo "Backup created: $ARCHIVE"
