# CalliCog setup - MacOS

## Install Homebrew

Go to the [Homebrew website](https://brew.sh/) and follow the instructions to install Homebrew.

Once it has been installed, refer to the output and follow any post-install instructions (e.g. adding `brew` to `.zshrc`).

## Install, configure Git

```sh
brew install git

git configure --global user.name "sccn@<computer name here>"
# Including computer name is helpful for keeping track of the origin of changes when some code edits are made
# from a shared environment
git configure --global user.email "<email address here>"
```

## Install, configure Postgres

```sh
brew install postgresql@15
brew services start postgresql@15
brew link postgresql@15 --force
/opt/homebrew/bin/createuser -s postgres
# ^ via: https://stackoverflow.com/questions/15301826/psql-fatal-role-postgres-does-not-exist
```

## Database setup

### When is a database instance required?
A CalliCog database instance is required for execution of commands and as the
backend for the webapp. If you don't need either on this machine, skip this
step (e.g. if you only want demo the software or are developing tasks).

### Create the database
CalliCog was built for use with Postgres. You can likely use another RDBMS, but it will require some customization.

If not already installed, install Postgres 15 or newer. For installation on a
MacOS host, [we recommend using brew](TODO insert link).

TODO consider how to make $USER universal for README

```sh
# Create `sccn` user:
psql -U postgres -c "CREATE ROLE sccn WITH SUPERUSER LOGIN"
# Create database:
createdb -U sccn callicog
```

## Install CalliCog

### Install Pyenv (recommended)
We recommend using `pyenv`, for control and isolation of different Python builds on a single machine.

Install [pyenv](pyenv_install).

```sh
# Install via Homebrew. See Pyenv docs for other install methods.
brew update
brew install pyenv
```

**IMPORTANT** After installing `pyenv`, [configure your shell environment](pyenv_cfg).

```sh
# Example for .zsh, the default shell of MacOS:
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

CalliCog has been
tested using Python `3.8.19`.

### Install Python (if needed)

**REQUIRED:** Python 3.8

CalliCog uses PsychoPy, which has a [narrow band of Python version support](ppy_py_vers). CalliCog has been tested with and supports Python 3.8.

Install Python 3.8.19 (if using `pyenv`):

**NOTE**: wxPython *requires* Python to be built with --enable-shared option.
```sh
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.8.19
```

### Clone, set up repository

```sh
git clone git@github.com:NIMH-SCCN/callicog.git
cd callicog

# If using `pyenv`, set the directory-local Python:
pyenv local 3.8.19

# Confirm local Python version is 3.8
python --version

# Create the virtual environment:
python -m venv .venv

# Activate the virtual environment:
source .venv/bin/activate
```

Install the required packages:
```sh
pip install PsychoPy==2021.2.3 --no-deps
pip install -r requirements.exec.txt
# Install the CalliCog package:
pip install -e .
```

### Why do it this way?
CalliCog uses the powerful, open-source [PsychoPy](ppy) as its cognitive task
engine. PsychoPy has [dependencies that can be difficult to wrangle](ppy_deps)
and which [effectively limit compatible Python versions](ppy_py_vers). For this
reason, CalliCog cannot be installed conventionally via e.g.
`pip install callicog`, but is instead installed as above.


[pyenv_install]: https://github.com/pyenv/pyenv?tab=readme-ov-file#installation
[pyenv_cfg]: https://github.com/pyenv/pyenv?tab=readme-ov-file#set-up-your-shell-environment-for-pyenv
[ppy]: TODO
[ppy_deps]: TODO
[ppy_py_vers]: TODO insert ppy forum post link here
