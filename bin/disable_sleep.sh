#!/bin/bash

echo 'DEPRECATION WARNING: Read comments inside this script file for info.'
# NOTE: I believe this has been superceded by the current configuration
# protocol as specified in the Ubuntu task-agent computer setup documentation.
# 
# I will leave this script in the repository for now for reference, in case
# for some reason we need to refer back to it.

# Check if DISPLAY is set (X server is running)
if [ -n "$DISPLAY" ]; then
    # Disable screen saver
    xset s off

    # Disable DPMS
    xset -dpms

    echo "Display Power Management and sleep disabled (Xorg)"
fi

# NOTE: if display is still sleeping/suspending, try running this command:
#
#   sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
#
# This command will "mask" or disable these settings persistently until they
# are re-enabled, meaning we don't need to re-run this after every reboot.
