# Agent PC Installation

The Agent PC requires [Ubuntu](https://ubuntu.com/desktop). Version 22.04 is the latest version supported, due to PsychoPy's [dependency on wxPython.](https://extras.wxpython.org/wxPython4/extras/linux/gtk3/)

## Installation

### Disable Wayland (re-enable X)

Most graphical Linux distros have for decades relied on a graphical system called Xorg or X. This display technology has architectural flaws, it is
being sunsetted in favor of a newer, more robust system called Wayland. Wayland is now the default graphics system in Ubuntu - but CalliCog is built on systems 
that are built on X, so we need to re-enable it. Fortunately, this is easy.

Open a terminal and edit this configuration file with your preferred editor, e.g. `nano`

```sh
sudo nano /etc/gdm3/custom.conf
```

You should see a line `#WaylandEnable=false`. Delete the `#` so the line is:

```sh
WaylandEnable=false
```

Save your changes and reboot the computer. This will disable Wayland and use
Xorg instead.

Upon reboot, confirm your changes succeeded:

```sh
$ echo $XDG_SESSION_TYPE
x11
# ^ you should see 'x11' here.
```

### Disable screen lock/sleep

Ensure that your display never goes to sleep, which would otherwise interfere with behavioral experiments.

* Disable screen lock/sleep: `Settings > Privacy > Screen`
* Blank Screen Delay:     `Never`
* Automatic Screen Lock:  `Off`

### Install software

Once running, open terminal and install the following tools.

```sh
sudo apt install git curl x11vnc openssh-client openssh-server screen vim stow
```

Clone the CalliCog repository.

```sh
git clone https://github.com/NIMH-SCCN/callicog.git
```


### Install Python 3.8.19 (supported version) using Pyenv

Referring to [the Pyenv documentation][pyenv], install `pyenv`. Edit your `.bashrc` and/or other configuration files as advised by the 
Pyenv installer.

Install Python build dependencies (required when Pyenv tries to build a
Python version). [Documentation is here][py_build_deps]. 

```sh
sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils \
tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```
> [!NOTE]
> if you run into a Python build issue, refer to the Pyenv documentation; these build dependencies could change with time.

Install Python 3.8.19.

    ```sh
    # Build/install an instance of Python 3.8.19:
    env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.8.19

    # Go to your CalliCog install directory:
    cd ~/callicog

    # Set the _directory-local_ Python version:
    pyenv local 3.8.19

    # Confirm Python version is 3.8.19:
    python --version
    ```
> [!NOTE]
> wxPython *requires* Python to be built with --enable-shared option.

### Build the CalliCog virtual environment

Create and activate the virtual environment:
```sh
cd ~/callicog
python3 -m venv .venv
source .venv/bin/activate

# Verify that when we invoke `python` now, it's the one in the venv:
which python
# ^ should give: `{install dir}/callicog/.venv/bin/python`

# Verify that it's still the correct version:
python --version
# ^ should give: `Python 3.8.19`
```

Install CalliCog's dependencies into the virtual environment:
```sh
pip install PsychoPy==2021.2.3 --no-deps
# Install most other requirements from file:
pip install -r requirements-linux.txt
```

Download the pre-built wheel for your Ubuntu version (22.04) and cPython (3.8):
```sh 
pip download https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-22.04/wxPython-4.2.0-cp38-cp38-linux_x86_64.whl

# Install the wheel file you downloaded:
pip install wxPython-4.2.0-cp38-cp38-linux_x86_64.whl

# Install libsdl, a dependency of wxPython:
sudo apt install libsdl2-2.0-0
```

Install the `callicog` package in editable mode:

```sh
# This invokes setup.py, enabling the `callicog` CLI command, among other things:
python setup.py install
pip install -e .
```

### Setup auto-start

Configure the Agent PC to automatically run CalliCog tools on boot.

```sh
source $HOME/callicog/.env
mkdir $HOME/.config/autostart
ln -s $CALLICOG_DIR/bin/install/callicog.desktop $HOME/.config/autostart/
ln -s $CALLICOG_DIR/bin/install/x11vnc.desktop $HOME/.config/autostart/
```

## Confirm installation

Run a test of CalliCog (ensure the virtual environment is active).

```sh
pytest tests/test_psychopy_click.py 
```

A window should open with a colored square stimulus, simulating a task as presented on the touchscreen. Click within the window to advance the task. After 3 windows, the test will end. 
If this sequence is observed, CalliCog is successfully installed.





[nano_cheat]:
https://web.archive.org/web/20240201142800/https://itsfoss.com/content/images/wordpress/2020/05/nano-cheatsheet.png
"Nano editor cheat sheet"
[wxpython_ubuntu]: https://extras.wxpython.org/wxPython4/extras/linux/gtk3/
"wxPython versions available for Ubuntu"
[ubuntu_usb]:
https://askubuntu.com/questions/1398432/how-to-burn-an-iso-file-to-a-usb
"Install Ubuntu via USB"
[new_ssh]:
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
"Generating a new SSH key"
[add_ssh]:
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
"Add an SSH key to your GitHub account"
[pyenv]: https://github.com/pyenv/pyenv
[py_build_deps]:
https://github.com/pyenv/pyenv/wiki#suggested-build-environment
[wxpy_blog]:
https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip/index.html
