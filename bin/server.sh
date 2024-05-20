#!/bin/bash

# This script simply starts the callicog task agent (aka 'the listener').

echo 'DEPRECATION PENDING: this script will be removed soon.'
# Now that the CLI interface has been improved, it is preferable to
# directly invoke these commands where needed, rather than obscuring
# them in an additional script layer.

# This may be needed for the Intel NUCs
#xrandr --output HDMI-2 --mode "1280x720"
source $HOME/callicog/.env      &&  \
source $CALLICOG_VENV/bin/activate  &&  \
callicog start agent --port=ttyACM0 --width=1280 --height=720 --dummy
