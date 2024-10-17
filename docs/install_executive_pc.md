# Executive PC Installation

The Executive PC requires a computer running macOS. CalliCog was last tested on Sonoma (v14.5).

## Installation

### Install pyenv (recommended)
We recommend using `pyenv`, for control and isolation of different Python builds on a single machine.

Install `pyenv`. This can be achieved easily using [Homebrew](https://brew.sh/) or alternative methods listed [here](https://github.com/pyenv/pyenv#installation)

```sh
brew update
brew install pyenv
```

After installing `pyenv`, [configure your shell environment](https://github.com/pyenv/pyenv?tab=readme-ov-file#set-up-your-shell-environment-for-pyenv).

```sh
# Example for .zsh, the default shell of MacOS:
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

### Install Python (if needed)
>[!Important]
> CalliCog uses PsychoPy, which has a [narrow band of Python version support](https://www.psychopy.org/download.html#pip-install). CalliCog has been tested with and supports **Python 3.8.19** (REQUIRED).

Install Python 3.8.19 (if using `pyenv`):
```sh
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.8.19
```
> [!NOTE]
> wxPython *requires* Python to be built with --enable-shared option.

### Clone git repository
```sh
git clone https://github.com/NIMH-SCCN/callicog.git
```

### Set up virtual environment
If using `pyenv`, set the directory-local Python:
```sh
cd callicog
pyenv local 3.8.19
```

```sh
# Confirm local Python version is 3.8
python --version

# Create the virtual environment:
python -m venv .venv

# Activate the virtual environment:
source .venv/bin/activate
```

Install the required packages:
```sh
pip install --upgrade pip
pip install PsychoPy==2021.2.3 --no-deps
pip install -r requirements-mac.txt
# Install the CalliCog package:
pip install -e .
```

### Create .env shell configuration file
```sh
# Enter your repo directory, e.g.:
cd ~/callicog
# Copy the .env.template to create the environment configuration file for this instance
cp .env.template .env \
&& echo "\n\n    Done. Now edit your .env file if customization needed for this environment (e.g. directory location, database name etc)."
```

### Why do it this way?
CalliCog uses the powerful, open-source [PsychoPy](https://www.psychopy.org/index.html) as its behavior task engine. PsychoPy has dependencies that can be difficult to wrangle, and which effectively limit compatible Python versions. For this reason, CalliCog cannot be installed conventionally (e.g. via `pip install callicog`), but is instead installed as above.

## Confirm installation
Run the CalliCog task "demo":

```sh
source .venv/bin/activate
callicog start demo
```
This should launch a Python window with an interactive stimulus. **If successful, CalliCog has been successfully installed.**

## Database setup

### Why is a database required?
A CalliCog database instance is required for execution of commands and as the
backend for the interactive webapp. It contains the behavioral data recorded from operant chambers, and the associated metadata (i.e. experimental design parameters set by the user). 
When the user interacts with the webapp, they are essentially interfacing with the database.

CalliCog was built for use with Postgres. You can likely use another RDBMS, but it will require some customization.

### Install and configure Postgres
```sh
brew install postgresql@15
brew services start postgresql@15
brew link postgresql@15 --force
/opt/homebrew/bin/createuser -s postgres
# ^ via: https://stackoverflow.com/questions/15301826/psql-fatal-role-postgres-does-not-exist
```

### Create the database
Run the `initdb.sh` script:
```sh
echo
echo "ATTENTION: database name, user, etc are configurable. Edit .env to customize before creating."
# cd to your repo directory, e.g.:
cd ~/callicog
./bin/initdb.sh
```
