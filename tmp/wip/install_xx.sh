#!/bin/bash

sudo apt-get install libsdl2-dev		&& \
python3 -m pip install --upgrade Pillow 	&& \
python3 -m pip install pyserial numpy 		&& \
python3 -m pip install matplotlib		&& \
python3 -m pip install pyqt5==5.14		&& \
# PsychoPy was freezing on "Attempting to measure
# frame rate of screen" message, see forums.
# Pinned until bug is fixed:
python3 -m pip install "psychopy==2022.2.4" --no-deps	&& \
# pyglet 2+ was causing problems:
# https://discourse.psychopy.org/t/import-error-cannot-import-name-gluerrorstring-from-pyglet-gl/31705
python3 -m pip install "pyglet<2"		&& \
python3 -m pip install arabic-reshaper		&& \
python3 -m pip install pyyaml requests freetype-py pandas python-bidi json-tricks scipy packaging future imageio pyzmq
