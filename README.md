# CalliCog #

This README would normally document whatever steps are necessary to get your application up and running.

### PostgreSQL instructions for Debian Stretch

	sudo apt-get install postgresql postgresql-client
	sudo -u postgres createuser --interactive
	pip install wheel
	pip install --upgrade pip
	pip install numpy psycopg2-binary SQLAlchemy flask flask-cors

### PostgreSQL instructions for macOS

	brew install postgresql
	brew services start postgresql
	createuser --interactive

### How to fix Homebrew in macOS (nuke and reinstall)

	sudo /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall.sh)"
	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
	brew update-reset

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

	sudo apt install python3-venv python3-pip
	python3.7 -m venv marmovenv
	source marmovenv/bin/activate
	pip install wheel
	python -m pip install --upgrade pip

Install Psychopy:

	sudo apt-get install libsdl2-dev
	python -m pip install --upgrade Pillow
	pip install pyserial numpy
	pip install matplotlib
	pip install pyqt5==5.14
	pip install psychopy --no-deps
	pip install pyyaml requests freetype-py pandas python-bidi pyglet json-tricks scipy packaging future imageio
	# download wxPython for Debian 10 (buster)
	wget https://extras.wxpython.org/wxPython4/extras/linux/gtk3/debian-10/wxPython-4.1.1-cp37-cp37m-linux_x86_64.whl
	pip install wxPython-4.1.1-cp37-cp37m-linux_x86_64.whl

Broadcast IP service:

	sudo systemctl edit --force --full broadcast_ip.service
	sudo systemctl enable broadcast_ip.service
	sudo systemctl start broadcast_ip.service
	sudo systemctl reboot