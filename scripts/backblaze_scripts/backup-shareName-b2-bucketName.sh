#!/bin/bash
echo "Deleting previous log"
rm {logLocation}/{shareName}_log.txt

echo "Running RClone Sync of {shareName} Share to B2 {shareName} Bucket"
rclone sync \
  --fast-list \
  --progress \
  --stats-one-line-date \
  --transfers 8 \
  --verbose \
  --exclude .Recycle.Bin/** \
  --links \
  --log-file {logLocation}/{shareName}_log.txt \
    /mnt/user/{shareName}/ \
    b2_buckets:{bucketName}

echo "Updating permissions of log file"
chmod 755 {logLocation}/{shareName}_log.txt