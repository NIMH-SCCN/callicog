#!/bin/bash

# Get wireless interface name (assuming wlan0)
wireless_interface="wlan0"

# Get wireless MAC address
wireless_mac=$(ifconfig $wireless_interface | grep ether | awk '{print $2}')

# Get serial number from CPU info
serial_number=$(cat /proc/cpuinfo | grep Serial | awk '{print $3}')

# Print results
echo "Wireless MAC:     $wireless_mac"
echo "Serial number:    $serial_number"
