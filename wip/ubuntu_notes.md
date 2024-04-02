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
- 
