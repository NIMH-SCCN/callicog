#!/bin/bash

CC_VENV_DEFAULT=".venv"

# Abort if not running on macOS
if [[ $(uname -s) != "Darwin" ]]; then
  echo "Error: This install script is intended for MacOS only."
  exit 1
fi


if command -v pyenv >/dev/null 2>&1; then
  # NOTE: --enable-shared is required per wxPython documentation
  env PYTHON_CONFIGURE_OPTS="--enable-shared"                             \
    pyenv install --skip-existing 3.8.19                                  &&
  pyenv local 3.8.19
else
  echo "pyenv is not installed."
  exit 1
fi

# Use alternative venv path if supplied as argument
CC_VENV="${1:-$CC_VENV_DEFAULT}"

python --version                                                        &&
python -m venv $CC_VENV                                                 &&
source .venv/bin/activate                                               &&
pip install --upgrade pip                                               &&
# PsychoPy is pinned becase TODO review notes for reason
pip install PsychoPy==2021.2.3 --no-deps                                &&
# pyglet is pinned because of an issue with PsychoPy
pip install "pyglet<1.6"                                                &&
# numpy is pinned because of an issue with PsychoPy
pip install numpy==1.21.6                                               &&
pip install Pillow pyserial matplotlib pyyaml requests freetype-py      \
  pandas python-bidi json-tricks scipy packaging future imageio         &&
# wxPython is pinned because TODO review notes for reason
pip install wxPython==4.2.0                                             &&
pip install PyQt5                                                       &&

# Direct dependencies of CalliCog:
pip install flask flask_cors flask_sqlalchemy psycopg2 pyzmq pytest                                                &&
pip install -e .
echo "CalliCog successfully installed in virtual environment $CC_VENV"
