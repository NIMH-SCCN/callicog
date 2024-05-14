#!/bin/bash

# Check if pyenv command exists
if ! command -v pyenv &> /dev/null; then
  echo "Error: pyenv is not installed or not configured correctly."
  echo "Please install pyenv following the official instructions: https://github.com/pyenv/pyenv"
  exit 1
fi

# Go to home dir:
cd ~

# Install Python build dependencies
sudo apt update
sudo apt install \
  build-essential \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  curl \
  libncursesw5-dev \
  xz-utils \
  tk-dev \
  libxml2-dev \
  libxmlsec1-dev \
  libffi-dev \
  liblzma-dev

# Build Python version with pyenv
#
#   !!! IMPORTANT: you must use --enable-shared !!!
#
#   see: https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip/index.html
#
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.11.8

# Install wxPython dependencies, see:
#
#   https://github.com/wxWidgets/Phoenix/blob/master/README.rst
#   https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip/
#
sudo apt install \
    dpkg-dev \
    build-essential \
    python3-dev \
    freeglut3-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libgstreamer-plugins-base1.0-dev \
    libgtk-3-dev \
    libjpeg-dev \
    libnotify-dev \
    libpng-dev \
    libsdl2-dev \
    libsm-dev \
    libtiff-dev \
    libwebkit2gtk-4.0-dev \
    libxtst-dev

# Set local python (local to working directory)
pyenv local 3.11.8

# MANUAL STEPS:
# # Create virtualenv
# pyenv virtualenv callicog
# 
# # Activate virtualenv
# pyenv activate callicog
# 
# # Install wxPython
# #
# #   see: https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip/index.html
# #
# pip install -U pip
# pip install -U six wheel setuptools
# pip download wxPython
# pip wheel -v wxPython-*  2>&1 | tee build.log
