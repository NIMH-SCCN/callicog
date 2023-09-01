#!/bin/bash

# Disable screen saver and DPMS
xset s off
xset -dpms

# NOTE: if display is still sleeping/suspending, try running this command:
# 
#   sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
#
# This command will "mask" or disable these settings persistently until they
# are re-enabled, meaning we don't need to re-run this after every reboot.
