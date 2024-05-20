# CalliCog Setup SOP

This SOP is intended to be separate from the README/repo documentation. It
should NOT be included in the official releases, as it may contain
SCCN-specific information, or just includes too much detail such that the
instructions can be either irrelevant, overwhelming or too brittle (e.g.
referring to official install instructions for Ubuntu is sufficient).

## Setting up the mini-PC

### Install Ubuntu

* Create an [installation USB][ubuntu_usb]
* Install Ubuntu via the USB drive


#### Navigate Ubuntu graphical install process
* Choose keyboard layout
    * English (US)
* Select "I don't want to connect to a Wi-Fi network right now"
    * Using either the white USB-A or black USB-C Ethernet adapters, plug the
mini-PC into the NIH network
    * Do not try to plug in via the built-in Ethernet port, this will not work
* Updates and other software
    * Minimal installation
    * Download updates while installing Ubuntu
    * Install third-party software for graphicxs and Wi-Fi hardware...
    * Configure secure boot with password "marmoset"
* Erase disk and install Ubuntu > Continue
* Select timezone (New York)
* Who are you?
    * Your name: ""
    * Your computer's name: "ccpcNN" (where NN is the appropriate number)
    * Pick a username: "sccn"
    * Log in automatically
    * Continue
* Reboot
* Remove installer USB, press enter to continue
* If prompted about MOK, press enter to continue
* Upon successful reboot, you will probably be prompted:
    * Software updates
        * Install software updates
    * Online Accounts
        * Skip
    * Ubuntu pro
        * Skip
    * Send system statistics/diagnostics?
        * No
    * Location services
        * Off
* If updates are installed, reboot if prompted


#### Disable Wayland (re-enable X)

Most graphical Linux distros have for decades relied on a graphical system
called Xorg or X. This display technology has architectural flaws, it is
being sunsetted in favor of a newer, more robust system called Wayland. Wayland
is now the default graphics system in Ubuntu--but CalliCog is built on systems
that are built on X, so we need to re-enable it. Fortunately, this is easy.

Open a terminal and edit a configuration file with your preferred editor:

```sh
sudo editor /etc/gdm3/custom.conf
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

* Disable screen lock/sleep: `Settings > Privacy > Screen`
  * Blank Screen Delay:		`Never`
  * Automatic Screen Lock:	`Off`

NOTE: If for some reason disabling sleep in the GUI doesn't work, try:
```sh
gsettings set org.gnome.settings-daemon.plugins.power		\
	sleep-inactive-ac-type 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power		\
	sleep-inactive-battery-type 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power		\
	sleep-inactive-ac-timeout 0
sudo systemctl mask sleep.target suspend.target					\
	hibernate.target hybrid-sleep.target
```


### Install software

* Once running, open terminal and install tools:
    ```sh
    sudo apt install git x11vnc screen vim stow
    ```

#### Clone the CalliCog repository

Contributing users (e.g. SCCN users) need to create an SSH key in order to use
the GitHub repository. While it is still private, this includes even cloning it
in the first place. Once we make it public, anyone will be able to clone it,
but only permissioned users will be able to push commits.

* [Create an SSH key][new_ssh], add it to the `ssh-agent`
* [Add the SSH key][add_ssh] to your GitHub account
* Clone CalliCog repo:
	```sh
	cd ~
	git clone git@github.com:NIMH-SCCN/callicog.git
	```


#### Install required Python version using Pyenv

* Referring to [the Pyenv documentation][pyenv], install `pyenv`.
  * Edit your `.bashrc` and/or other configuration files as advised by the 
Pyenv installer.
    * This adds the `pyenv` install directory to your `$PATH`, so your shell
will know where to look to find it when you type the command "pyenv" on the
command line
* Install Python build dependencies (required when Pyenv tries to build a
Python version). [Documentation is here][py_build_deps]. 
	```sh
    # NOTE: if you run into a Python build issue, refer to the Pyenv
    # documentation; these build dependencies could change with time.
	sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
	libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils \
    tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
	```
* Install the required Python version, 3.8.19. NOTE: `--enable-shared` argument
is *required*, [per wxPython][wxpy_blog].
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

#### Build the CalliCog virtual environment

* Create and activate the virtual environment:
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
* Install CalliCog's dependencies into the virtual environment:
    ```sh
    pip install PsychoPy==2021.2.3 --no-deps
    pip install Pillow pyserial numpy==1.21.6 matplotlib pyqt5==5.14.0 pyyaml       \
        requests freetype-py pandas python-bidi pyglet==1.4.11 json-tricks  \
        scipy packaging future imageio pyzmq pytest Click
    ```

* Continuing with installing dependencies, this one has historically been finnicky. See note below if this snippet fails to install:
    ```sh
    # Download the pre-built wheel for your Ubuntu version (22.04) and cPython (3.8):
    pip download https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-22.04/wxPython-4.2.0-cp38-cp38-linux_x86_64.whl

    # Install the wheel file you downloaded:
    pip install wxPython-4.2.0-cp38-cp38-linux_x86_64.whl

    # Install libsdl, a dependency of wxPython:
    sudo apt install libsdl2-2.0-0
    ```

* Install the `callicog` package in editable mode:

   ```sh
   # This invokes setup.py, enabling the `callicog` CLI command, among other things
   pip install -e .
   ```

* Now let's run a test of CalliCog:
    ```sh
    pytest tests/test_psychopy_click.py 
    ```

A window should open with a colored square stimulus, simulating a task as presented on the touchscreen. Click within the window to advance the task. After 3 windows the test will end.  

#### Setup auto-start

Set the CalliCog shell environment variables, make the special `autostart` directory, and then create symlinks to the `*.desktop` files that run on startup.

sh
```
source $HOME/callicog/.env
mkdir $HOME/.config/autostart
ln -s $CALLICOG_DIR/bin/install/callicog.desktop $HOME/.config/autostart/
ln -s $CALLICOG_DIR/bin/install/vnc_autostart.desktop $HOME/.config/autostart/
```


### Links
[ubuntu_usb]: https://askubuntu.com/questions/1398432/how-to-burn-an-iso-file-to-a-usb "Install Ubuntu via USB"
[new_ssh]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent "Generating a new SSH key"
[add_ssh]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account "Add an SSH key to your GitHub account"
[pyenv]: https://github.com/pyenv/pyenv
[py_build_deps]: https://github.com/pyenv/pyenv/wiki#suggested-build-environment
[wxpy_blog]: https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip/index.html
