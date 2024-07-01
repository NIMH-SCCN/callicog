#!/bin/bash

# This script simply starts the callicog task agent (aka 'the listener').

# Read the CalliCog configuration variables into the shell environment:
source $HOME/callicog/.env

# Tell the X server what display mode to use for which output:
model_info=$(hostnamectl | grep "Hardware Model")
if [[ $model_info =~ "NUC" ]]; then
  # Running on Intel NUC
  xrandr --output $CALLICOG_DISPLAY --mode "1280x720"
elif [[ $model_info =~ "Meerkat" ]]; then
  # Running on System76 Meerkat (also Intel NUC)
  xrandr --output $CALLICOG_DISPLAY --mode "1280x720"
else
  :  # pass
fi

# Activate the virtual environment and start the task agent:
source $CALLICOG_VENV/bin/activate
callicog start agent	\
  --port=ttyACM0	\
  --width=1280		\
  --height=720		\
  --fullscreen

# !!! NOTE !!! for debugging/dev, to run without a reward module,
# add this line above the --fullscreen line:
#
#  --dummy		\
