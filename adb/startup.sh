#!/bin/sh

DEVICES='SHIELD.singularity.net'

echo "Starting up ADB..."

while true; do
  adb -a server nodaemon > /dev/null 2>&1
  sleep 10
done &

echo "Server started. Waiting for 30 seconds..."
sleep 30

echo "Connecting to devices."
for device in $DEVICES; do
   adb connect $device
done
echo "Done."

while true; do
  for device in $DEVICES; do
    adb connect $device > /dev/null 2>&1
  done
  sleep 60
done

