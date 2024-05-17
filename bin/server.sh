#!/bin/bash

# This may be needed for the Intel NUCs
#xrandr --output HDMI-2 --mode "1280x720"
source ~/callicog/callicog.env      &&  \
source $CALLICOG_VENV/bin/activate  &&  \
callicog start agent --port=ttyACM0 --width=1280 --height=720 --dummy
