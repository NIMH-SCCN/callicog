#!/bin/bash

# NOTE: --enable-shared is required per wxPython documentation
# env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.8.19        &&
pyenv local 3.8.19                                                      &&
python --version                                                        &&
python -m venv .venv                                                    &&
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
pip install pyzmq pytest                                                &&
pytest tests/test_psychopy_click.py 
