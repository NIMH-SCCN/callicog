# CalliCog setup - MacOS

## Database setup

### When is a database instance required?
A CalliCog database instance is required for execution of commands and as the
backend for the webapp. If you don't need either on this machine, skip this
step (e.g. if you only want demo the software or are developing tasks).

### Create the database
CalliCog was built for use with Postgres.

If not already installed, install Postgres 15 or newer. For installation on a
MacOS host, [we recommend using brew](TODO insert link).

TODO consider how to make $USER universal for README

To create a new instance of the CalliCog database.
- TODO finish this

## Install CalliCog

CalliCog requires Python 3.8. We recommend using [pyenv](pyenv), for control
and isolation of different Python builds on a single machine. CalliCog has been
tested using Python `3.8.19`.

To install Python 3.8.19 using `pyenv`:

```
# NOTE: wxPython *requires* Python to be built with --enable-shared option
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.8.19
```

Open a terminal window and `cd` to the directory you want to install into.
Clone the repository.

```
# Clone the repository
git clone git@github.com:NIMH-SCCN/callicog.git
# cd into the repository dir
cd callicog
```

If using pyenv:
```
# Set the directory-local Python
pyenv local 3.8.19
```

```
# Confirm local Python version is 3.8
python --version
# Run the virtualenv install script
./bin/install/dependencies-mac.sh
```

- Install 
- build python 3.8
- set local python
- create venv
- activate

### Why do it this way?
CalliCog uses the powerful, open-source [PsychoPy](ppy) as its cognitive task
engine. PsychoPy has [dependencies that can be difficult to wrangle](ppy_deps)
and which [effectively limit compatible Python versions](ppy_py_vers). For this
reason, CalliCog cannot be installed conventionally via e.g.
`pip install callicog`, but is instead installed as above.
```
pip install PsychoPy==2021.2.3 --no-deps
pip install "pyglet<1.6"
pip install numpy==1.21.6
pip install Pillow pyserial matplotlib pyyaml requests freetype-py \
  pandas python-bidi json-tricks scipy packaging future imageio
pip install wxPython==4.2.0
pip install pyzmq pytest
cd callicog/
pytest tests/test_psychopy_click.py 
```

