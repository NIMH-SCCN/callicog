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

```shell
sudo editor /etc/gdm3/custom.conf
```

You should see a line `#WaylandEnable=false`. Delete the `#` so the line is:

```shell
WaylandEnable=false
```

Save your changes and reboot the computer. This will disable Wayland and use
Xorg instead.

Upon reboot, confirm your changes succeeded:

```shell
$ echo $XDG_SESSION_TYPE
x11
# ^ you should see 'x11' here.
```


### Install software

* Once running, open terminal and install tools:
    ```shell
    sudo apt install git screen vim stow
    ```

#### Clone the CalliCog repository

Contributing users (e.g. SCCN users) need to create an SSH key in order to use
the GitHub repository. While it is still private, this includes even cloning it
in the first place. Once we make it public, anyone will be able to clone it,
but only permissioned users will be able to push commits.

* [Create an SSH key][new_ssh], add it to the `ssh-agent`
* [Add the SSH key][add_ssh] to your GitHub account
* Clone CalliCog repo:
	```shell
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
	```shell
    # NOTE: if you run into a Python build issue, refer to the Pyenv
    # documentation; these build dependencies could change with time.
	sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
	libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils \
    tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
	```
* Install the required Python version, 3.8.19. NOTE: `--enable-shared` argument
is *required*, [per wxPython][wxpy_blog].
    ```shell
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
    ```shell
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
    pip install Pillow pyserial numpy matplotlib pyqt5==5.14.0 pyyaml       \
        requests freetype-py pandas python-bidi pyglet==1.4.11 json-tricks  \
        scipy packaging future imageio
    pip install pyzmq
    pip install pytest
    pip install wxPython-4.2.0-cp38-cp38-linux_x86_64.whl
    cd callicog/
    pytest tests/test_psychopy_click.py 
    pip uninstall numpy
    pip install numpy==1.21.6
    pytest tests/test_psychopy_click.py 
    ```

#### Configure OS for use in CalliCog context




* 

	```shell 
	sudo ln -s ~/callicog/scripts/broadcastIP_slack ~       &&
	sudo ln -s ~/callicog/scripts/start_callicog_server ~   &&
	sudo ln -s ~/callicog/scripts/changeres.sh ~            &&
	sudo ln -s ~/callicog/scripts/flush.sh ~                &&
	sudo ln -s ~/callicog/scripts/kill_callicog.sh ~        &&
	sudo ln -s ~/callicog/scripts/start_vncserver.sh
	```

* Disable screen lock/sleep: Settings > Privacy > Screen
* Install CalliCog dependencies:

	```shell
	cd ~                                                    && 
	sudo apt install python3 python3-venv python3-pip       &&
	python3 -m venv callicogenv                             &&
	source callicogenv/bin/activate                 	&&
	pip install --upgrade pip				&&
	pip install wheel
	```

* Install wxPython:

	* Identify your Ubuntu version number, e.g. 22.04
	* Identify your Python3 major version number, e.g. 3.10
	- NOTE!: If using `pyenv`, be sure the Python you're using was
	    compiled with the `--enable-shared` argument, e.g.:
		`env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.10.12`
	- Download a .whl wheel file that corresponds:
		- Go to: https://extras.wxpython.org/wxPython4/extras/linux/gtk3
		- Click on the directory matching your OS version
		- Identify a file compiled for your Python3 version,
		  for Python 3.10, this would have `cp310` in the filename
		- Copy the url of the file you've selected
		- Run:
			`pip download {pasted url}` 
	- Now install:
			`pip install {downloaded .whl filename}`
- Install PsychoPy:

	```shell
	sudo apt install libsdl2-dev	&&
	pip install pyyaml requests freetype-py pandas python-bidi json-tricks scipy packaging future imageio pyserial numpy matplotlib pyqt5 &&
	pip install "pyglet==1.5.27"	&&
	pip install psychopy --no-deps
	```
- NOTE: some steps are missing between this step and where I ultimately got, which was up to the point where I could run CalliCog tasks BUT PsychoPy registered no mouse input. I was able to narrow this down to a problem with the CalliCog repository, since I downloaded the PsychoPy git repo and was able to run mouse-specific demo scripts perfectly well. I was not able to determine the origin of this problem in the tangle of PsychoPy code throughout CalliCog, so I am instead attempting to recreate the identical virtualenv to ccpc01, which was setup most recently and which is working. It uses Python 3.7.3. There is a snapshot of the requirements in wip/ccpc01.requirements.txt. The following notes will detail my attempt to recreate this environment exactly:
- First, install the Pyenv dependencies:

	```shell
	# Install Pyenv's build dependencies (required when Pyenv tries to build a python version).
	# Documentation is here, in case troubleshooting is needed:
	#     https://github.com/pyenv/pyenv/wiki#suggested-build-environment
	sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
	libbz2-dev libreadline-dev libsqlite3-dev curl \
	libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
	```
- Next, install Pyenv

	```shell
	# NOTE: be sure to edit both .bashrc and .profile according to the instructions provided by the installer after it runs:
	curl https://pyenv.run | bash
	```

- Next, install Python 3.7.3:

	```shell
	# NOTE: I used CC=clang because I ran into issues using the default compiler, which I believe is gcc. See:
	#     https://github.com/pyenv/pyenv/issues/1889#issuecomment-833587851
	# Also, I used `--enable-shared` because wxPython specifies that it should be used if using Pyenv
	#     https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip/index.html
	sudo apt install clang
	env CC="clang" PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.7.3

- Next, set the local python version, create the virtualenv, activate virtualenv:

	```shell
	# TODO
	```

- Now, install wxPython

	```sh
	# TODO
	# - install wxPython dependencies
	# - attempt to build a wheel for wxPython for Python 3.7.3 using instructions on wxPython blog
	# - failed!
	```
- I remembered that I had previously downloaded and archived a wheel for 3.7.3, so I tried installing using that. Install went fine, but on running tests there was an issue emanating from wxPython:

```sh
sccn@ccpc05:~/callicog$ pytest tests/test_psychopy_click.py
======================================================================================= test session starts =======================================================================================
platform linux -- Python 3.7.3, pytest-7.4.4, pluggy-1.2.0
rootdir: /home/sccn/callicog
collected 1 item

tests/test_psychopy_click.py F                                                                                                                                                              [100%]

============================================================================================ FAILURES =============================================================================================
___________________________________________________________________________________________ test_touch2 ___________________________________________________________________________________________

    def test_touch2():
        from tasks.touch2 import TaskInterface
>       from marmobox_interface import MarmoboxInterface

tests/test_psychopy_click.py:39:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
marmobox_interface.py:5: in <module>
    from psychopy import visual, event
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/visual/__init__.py:29: in <module>
    from psychopy import event  # import before visual or
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/event.py:70: in <module>
    from psychopy.tools.monitorunittools import cm2pix, deg2pix, pix2cm, pix2deg
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/tools/monitorunittools.py:15: in <module>
    from psychopy import monitors
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/monitors/__init__.py:10: in <module>
    from .calibTools import *
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/monitors/calibTools.py:21: in <module>
    from psychopy import __version__, logging, hardware, constants
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/hardware/__init__.py:13: in <module>
    from . import eyetracker
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/hardware/eyetracker.py:2: in <module>
    from psychopy.alerts import alert
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/alerts/__init__.py:5: in <module>
    from ._alerts import alert, catalog
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/alerts/_alerts.py:11: in <module>
    from psychopy.localization import _translate
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/localization/__init__.py:23: in <module>
    import wx
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/wx/__init__.py:17: in <module>
    from wx.core import *
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    """

>   from ._core import *
E   ImportError: libjpeg.so.62: cannot open shared object file: No such file or directory

../.pyenv/versions/3.7.3/lib/python3.7/site-packages/wx/core.py:12: ImportError
===================================================================================== short test summary info =====================================================================================
FAILED tests/test_psychopy_click.py::test_touch2 - ImportError: libjpeg.so.62: cannot open shared object file: No such file or directory
======================================================================================== 1 failed in 0.26s ========================================================================================
```

- Attempts using 3.7.3 failed, so I am going to attempt instead to use Python 3.8, which has a pre-built wheel hosted on wxPython site. Hopefully this doesn't impair my abilitiy to install the identical ccpc01.requirements.txt

- Install python 3.8.19

```sh
sccn@ccpc05:~$ env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.8.19
# NOTE: succeeded without needing clang
```

- Set local python, create, activate venv:

```sh
#TODO recap
```

- Install, starting with pinned PsychoPy so subsequent dependencies are constrained re: versions

```sh
pip install PsychoPy==2021.2.3 --no-deps
pip install Pillow pyserial numpy matplotlib pyqt5==5.14.0 pyyaml requests freetype-py pandas python-bidi pyglet==1.4.11 json-tricks scipy packaging future imageio
pip install pyzmq
pip install pytest
pip install wxPython-4.2.0-cp38-cp38-linux_x86_64.whl 
cd callicog/
pytest tests/test_psychopy_click.py 
pip uninstall numpy
pip install numpy==1.21.6
pytest tests/test_psychopy_click.py 
```


#### Navigate Ubuntu graphical install process
- Choose keyboard layout
    - English (US)
- Select "I don't want to connect to a Wi-Fi network right now"
    - Using either the white USB-A or black USB-C Ethernet adapters, plug the
mini-PC into the NIH network
    - Do not try to plug in via the built-in Ethernet port, this will not work
- Updates and other software
    - Minimal installation
    - Download updates while installing Ubuntu
    - Install third-party software for graphicxs and Wi-Fi hardware...
    - Configure secure boot with password "marmoset"
- Erase disk and install Ubuntu > Continue
- Select timezone (New York)
- Who are you?
    - Your name: ""
    - Your computer's name: "ccpcNN" (where NN is the appropriate number)
    - Pick a username: "sccn"
    - Log in automatically
    - Continue
- Reboot
- Remove installer USB, press enter to continue
- If prompted about MOK, press enter to continue
- Upon successful reboot, you will probably be prompted:
    - Software updates
        - Install software updates
    - Online Accounts
        - Skip
    - Ubuntu pro
        - Skip
    - Send system statistics/diagnostics?
        - No
    - Location services
        - Off
- If updates are installed, reboot if prompted


#### Disable Wayland (re-enable X)

Most graphical Linux distros have for decades relied on a graphical system
called Xorg or X. This display technology has architectural flaws, it is
being sunsetted in favor of a newer, more robust system called Wayland. Wayland
is now the default graphics system in Ubuntu--but CalliCog is built on systems
that are built on X, so we need to re-enable it. Fortunately, this is easy.

Open a terminal and edit a configuration file with your preferred editor:

```shell
sudo editor /etc/gdm3/custom.conf
```

You should see a line `#WaylandEnable=false`. Delete the `#` so the line is:

```shell
WaylandEnable=false
```

Save your changes and reboot the computer. This will disable Wayland and use
Xorg instead.

Upon reboot, confirm your changes succeeded:

```shell
$ echo $XDG_SESSION_TYPE
x11
# ^ you should see 'x11' here.
```


#### Install required software

- Once running, open terminal and install tools:

	`sudo apt install git screen vim stow`

- Set up an ssh key (TODO, add link to GitHub instructions)
    - https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
- Clone CalliCog repo:

	```shell
	cd ~
	git clone git@github.com:NIMH-SCCN/callicog.git
	```

- 

	```shell 
	sudo ln -s ~/callicog/scripts/broadcastIP_slack ~       &&
	sudo ln -s ~/callicog/scripts/start_callicog_server ~   &&
	sudo ln -s ~/callicog/scripts/changeres.sh ~            &&
	sudo ln -s ~/callicog/scripts/flush.sh ~                &&
	sudo ln -s ~/callicog/scripts/kill_callicog.sh ~        &&
	sudo ln -s ~/callicog/scripts/start_vncserver.sh
	```

- Disable screen lock/sleep: Settings > Privacy > Screen
- Install CalliCog dependencies:

	```shell
	cd ~                                                    && 
	sudo apt install python3 python3-venv python3-pip       &&
	python3 -m venv callicogenv                             &&
	source callicogenv/bin/activate                 	&&
	pip install --upgrade pip				&&
	pip install wheel
	```

- Install wxPython:

	- Identify your Ubuntu version number, e.g. 22.04
	- Identify your Python3 major version number, e.g. 3.10
	- NOTE!: If using `pyenv`, be sure the Python you're using was
	    compiled with the `--enable-shared` argument, e.g.:
		`env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.10.12`
	- Download a .whl wheel file that corresponds:
		- Go to: https://extras.wxpython.org/wxPython4/extras/linux/gtk3
		- Click on the directory matching your OS version
		- Identify a file compiled for your Python3 version,
		  for Python 3.10, this would have `cp310` in the filename
		- Copy the url of the file you've selected
		- Run:
			`pip download {pasted url}` 
	- Now install:
			`pip install {downloaded .whl filename}`
- Install PsychoPy:

	```shell
	sudo apt install libsdl2-dev	&&
	pip install pyyaml requests freetype-py pandas python-bidi json-tricks scipy packaging future imageio pyserial numpy matplotlib pyqt5 &&
	pip install "pyglet==1.5.27"	&&
	pip install psychopy --no-deps
	```
- NOTE: some steps are missing between this step and where I ultimately got, which was up to the point where I could run CalliCog tasks BUT PsychoPy registered no mouse input. I was able to narrow this down to a problem with the CalliCog repository, since I downloaded the PsychoPy git repo and was able to run mouse-specific demo scripts perfectly well. I was not able to determine the origin of this problem in the tangle of PsychoPy code throughout CalliCog, so I am instead attempting to recreate the identical virtualenv to ccpc01, which was setup most recently and which is working. It uses Python 3.7.3. There is a snapshot of the requirements in wip/ccpc01.requirements.txt. The following notes will detail my attempt to recreate this environment exactly:
- First, install the Pyenv dependencies:

	```shell
	# Install Pyenv's build dependencies (required when Pyenv tries to build a python version).
	# Documentation is here, in case troubleshooting is needed:
	#     https://github.com/pyenv/pyenv/wiki#suggested-build-environment
	sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
	libbz2-dev libreadline-dev libsqlite3-dev curl \
	libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
	```
- Next, install Pyenv

	```shell
	# NOTE: be sure to edit both .bashrc and .profile according to the instructions provided by the installer after it runs:
	curl https://pyenv.run | bash
	```

- Next, install Python 3.7.3:

	```shell
	# NOTE: I used CC=clang because I ran into issues using the default compiler, which I believe is gcc. See:
	#     https://github.com/pyenv/pyenv/issues/1889#issuecomment-833587851
	# Also, I used `--enable-shared` because wxPython specifies that it should be used if using Pyenv
	#     https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip/index.html
	sudo apt install clang
	env CC="clang" PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.7.3

- Next, set the local python version, create the virtualenv, activate virtualenv:

	```shell
	# TODO
	```

- Now, install wxPython

	```sh
	# TODO
	# - install wxPython dependencies
	# - attempt to build a wheel for wxPython for Python 3.7.3 using instructions on wxPython blog
	# - failed!
	```
- I remembered that I had previously downloaded and archived a wheel for 3.7.3, so I tried installing using that. Install went fine, but on running tests there was an issue emanating from wxPython:

```sh
sccn@ccpc05:~/callicog$ pytest tests/test_psychopy_click.py
======================================================================================= test session starts =======================================================================================
platform linux -- Python 3.7.3, pytest-7.4.4, pluggy-1.2.0
rootdir: /home/sccn/callicog
collected 1 item

tests/test_psychopy_click.py F                                                                                                                                                              [100%]

============================================================================================ FAILURES =============================================================================================
___________________________________________________________________________________________ test_touch2 ___________________________________________________________________________________________

    def test_touch2():
        from tasks.touch2 import TaskInterface
>       from marmobox_interface import MarmoboxInterface

tests/test_psychopy_click.py:39:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
marmobox_interface.py:5: in <module>
    from psychopy import visual, event
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/visual/__init__.py:29: in <module>
    from psychopy import event  # import before visual or
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/event.py:70: in <module>
    from psychopy.tools.monitorunittools import cm2pix, deg2pix, pix2cm, pix2deg
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/tools/monitorunittools.py:15: in <module>
    from psychopy import monitors
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/monitors/__init__.py:10: in <module>
    from .calibTools import *
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/monitors/calibTools.py:21: in <module>
    from psychopy import __version__, logging, hardware, constants
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/hardware/__init__.py:13: in <module>
    from . import eyetracker
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/hardware/eyetracker.py:2: in <module>
    from psychopy.alerts import alert
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/alerts/__init__.py:5: in <module>
    from ._alerts import alert, catalog
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/alerts/_alerts.py:11: in <module>
    from psychopy.localization import _translate
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/psychopy/localization/__init__.py:23: in <module>
    import wx
../.pyenv/versions/3.7.3/lib/python3.7/site-packages/wx/__init__.py:17: in <module>
    from wx.core import *
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    """

>   from ._core import *
E   ImportError: libjpeg.so.62: cannot open shared object file: No such file or directory

../.pyenv/versions/3.7.3/lib/python3.7/site-packages/wx/core.py:12: ImportError
===================================================================================== short test summary info =====================================================================================
FAILED tests/test_psychopy_click.py::test_touch2 - ImportError: libjpeg.so.62: cannot open shared object file: No such file or directory
======================================================================================== 1 failed in 0.26s ========================================================================================
```

- Attempts using 3.7.3 failed, so I am going to attempt instead to use Python 3.8, which has a pre-built wheel hosted on wxPython site. Hopefully this doesn't impair my abilitiy to install the identical ccpc01.requirements.txt

- Install python 3.8.19

```sh
sccn@ccpc05:~$ env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.8.19
# NOTE: succeeded without needing clang
```

- Set local python, create, activate venv:

```sh
#TODO recap
```

- Install, starting with pinned PsychoPy so subsequent dependencies are constrained re: versions

```sh
pip install PsychoPy==2021.2.3 --no-deps
pip install Pillow pyserial numpy matplotlib pyqt5==5.14.0 pyyaml requests freetype-py pandas python-bidi pyglet==1.4.11 json-tricks scipy packaging future imageio
pip install pyzmq
pip install pytest
pip install wxPython-4.2.0-cp38-cp38-linux_x86_64.whl 
cd callicog/
pytest tests/test_psychopy_click.py 
pip uninstall numpy
pip install numpy==1.21.6
pytest tests/test_psychopy_click.py 
```


### Links
[ubuntu_usb]: https://askubuntu.com/questions/1398432/how-to-burn-an-iso-file-to-a-usb "Install Ubuntu via USB"
[new_ssh]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent "Generating a new SSH key"
[add_ssh]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account "Add an SSH key to your GitHub account"
[pyenv]: https://github.com/pyenv/pyenv
[py_build_deps]: https://github.com/pyenv/pyenv/wiki#suggested-build-environment
[wxpy_blog]: https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip/index.html
