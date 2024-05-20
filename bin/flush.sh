#!/bin/bash

echo 'DEPRECATION PENDING: this script will be removed soon.'
# Now that the CLI interface has been improved, it is preferable to
# directly invoke these commands where needed, rather than obscuring
# them in an additional script layer.


source $HOME/callicog/.env      &&  \
source $CALLICOG_VENV/bin/activate  &&  \
callicog flush "$@"
