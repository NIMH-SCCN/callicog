#!/bin/bash

# This script is just a convenience, it activates the virtual
# environment and then invokes the `callicog` command,
# passing through any arguments supplied.

source $HOME/callicog/.env		&&  \
source $CALLICOG_VENV/bin/activate	&&  \
callicog "$@"
