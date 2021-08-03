# CalliCog #

This README would normally document whatever steps are necessary to get your application up and running.

### Fresh install

	sudo apt install python3-venv python3-pip
	python3 -m venv marmovenv

### PostgreSQL instructions for Ubuntu 18.04

	sudo apt-get install postgresql-client-11 postgresql-11
	sudo -u postgres createuser --interactive

### PostgreSQL instructions for Debian Stretch

	sudo apt-get install postgresql postgresql-client libpq-dev python-dev
	sudo -u postgres createuser --interactive
	pip install psycopg2-binary SQLAlchemy
	./createdb.sh
	./psql.sh

### Copy files to Google Drive with `rclone`

Full documentation [here](https://rclone.org/drive/).

	sudo apt-get update
	sudo apt-get install rclone

### Raspberry Pi Zero headless setup

Insert SD card and in the `boot` partition create the file `wpa_supplicant.conf` and include this:

	country=AU
	ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
	update_config=1
	network={
		ssid="MyWiFiNetwork"
		psk="aVeryStrongPassword"
		key_mgmt=WPA-PSK
	}

Create another empty file called `ssh`.

### Raspberry Pi Zero Camera V2 setup
	
	sudo raspi-config # Interfacing -> Enable Camera
	ls /lib/modules/`uname -r`/kernel/drivers/media/platform/bcm2835 # check V4L2 kernel module
	raspivid --width 640 --height 360 --framerate 24 --bitrate 750000 --qp 20 --timeout $((10*1000)) --output vid.h264

### Install `motion` to livestream

	wget https://github.com/Motion-Project/motion/releases/download/release-4.1.1/pi_jessie_motion_4.1.1-1_armhf.deb
	sudo apt-get install gdebi-core
	sudo gdebi pi_jessie_motion_4.1.1-1_armhf.deb
	mkdir ~/.motion && cp /etc/motion/motion.conf ~/.motion/motion.conf
	mkdir ~/motionvid
	nano ~/.motion/motion.conf

More info regardin the configuration file [here](https://www.bouvet.no/bouvet-deler/utbrudd/building-a-motion-activated-security-camera-with-the-raspberry-pi-zero).

### Install OpenCV in the Raspberry Pi Zero

Full documentation [here](https://towardsdatascience.com/installing-opencv-in-pizero-w-8e46bd42a3d3)

### Install firmata and pyfirmata

Under Linux, give current user access to COM ports:

	sudo gpasswd --add ${USER} dialout

Upload Standard Firmata code from Arduino IDE. Then execute `pip install pyfirmata`.

### Intel MiniPC setup

Install latest Python 3 version via source package found [here](https://www.python.org/downloads/source/):

	sudo apt-get update
	sudo apt-get upgrade
	sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl libbz2-dev liblzma-dev
	curl -O [python-tarxz-url]
	tar -xf Python-3.8.6.tar.xz
	cd Python-3.8.6
	./configure --enable-optimizations
	make -j `nproc`
	sudo make altinstall
	python3.8 --version

Create the `marmovenv` virtual environment:

	python3.8 -m venv marmovenv
	source marmovenv/bin/activate
	pip install wheel
	python -m pip install --upgrade pip

Install Psychopy:

	sudo apt-get install libsdl2-dev
	pip install pyserial matplotlib numpy
	pip install pyqt5==5.14
	pip install psychopy --no-deps
	pip install pyyaml requests freetype-py pandas python-bidi pyglet json-tricks scipy packaging future imageio
	# download wxPython for Debian 10 (buster)
	wget https://extras.wxpython.org/wxPython4/extras/linux/gtk3/debian-10/wxPython-4.1.1-cp37-cp37m-linux_x86_64.whl
	pip install wxPython-4.1.1-cp37-cp37m-linux_x86_64.whl

### Progression logic

- Rolling average
	- inputs: number of trials, success criterion, sample size
	- evaluation
		1. 
- Global success
