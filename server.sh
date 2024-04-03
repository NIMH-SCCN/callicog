#!/bin/bash

# This may be needed for the Intel NUCs
#xrandr --output HDMI-2 --mode "1280x720"
python3 marmobox_listener.py ttyACM0 --fullscreen
# python3 marmobox_listener.py ttyACM0 --fullscreen --dummy
