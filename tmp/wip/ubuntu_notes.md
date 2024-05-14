# Attempting Intel NUC setup on Ubuntu

Previous attempt to run CalliCog on Debian was plagued with difficulties. These can be attributed broadly to two factors:

1. CalliCog dependencies
2. Debian is not formally supported on Intel NUC

Very "stale", lots of changes to direct and indirect dependencies since README was last updated. This means that some of our direct dependencies which had to be pinned (a specific version or version range is specified) for one reason or another would conflict with the latest version of other CalliCog dependencies. Often this was not identified by pip, but only appeared at runtime, for example when an older version of PsychoPy would invoke `np.float` from Numpy, an interface which changed in version 1.20 of Numpy. After several iterations of handling such conflicts, I was able to get the CalliCog listener running. Then, when I trialed an actual request from the server to the listener, I encountered an error with PsychoPy that I *think* is related to how PsychoPy attempts to interpret the system's video drivers/configuration. Because Debian is not an explicitly supported OS for the Intel NUCs, there was always a risk that there would be problems with drivers for the hardware. I was optimistic about this, since Ubuntu is supported and there are Intel drivers for Ubuntu, and Ubuntu is built on Debian. Despite my attempts to identify and install drivers under Debian for the NUC, I did not succeed beyond a package of generic drivers for Intel hardware that is part of the standard Debian distribution. This means that basic features of the integrated GPU were able to be used, but probably not efficiently, and the system was never able to identify the graphics device, so any commands that would normally query or configure it would either fail, or return generic information. The display was configured at a default resolution which was unchangeable. I believe this is where PsychoPy was choking--it was probably querying some system library to get information like the display resolution, and then when it would try to determine how to scale the objects it was trying to draw, the code didn't account for this case and fail to some default--it made an erroneous assumption in a conditional, throwing a fatal error.

So it was at this stage that I decided to try Ubuntu, in hopes that as an officially supported OS, this issue at least would be obviated. Being based on Debian, my hope is that there will not be many changes needed to the installation protocol.

## Installing on Ubuntu

So far, the first signs are good.


- Create a (bootable USB)[https://askubuntu.com/questions/1398432/how-to-burn-an-iso-file-to-a-usb]
- Install Ubuntu via the USB
- Install the proprietary packages when prompted, using a memorable password
- When prompted
	- create the user `{username}`
	- name the computer `{pcname}`, and
	- enable automatic login
- Connect to internet
	- if wifi is required, enable it (TODO, add instructions from AskUbuntu)
- Once running, open terminal and install tools:

	`sudo apt install git screen vim stow`

- Set up an ssh key (TODO, add link to GitHub instructions)
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

