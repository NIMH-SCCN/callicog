# CalliCog #

### Pre installation: create bootable Debian drive

Flash USB with Debian 10.11 (Buster) [ISO file](https://drive.google.com/file/d/1hRkasJ1nOOUxclgPgWfXA9Y2jxiqqZsI/view?usp=sharing) using [balenaEtcher](https://www.balena.io/etcher/).

### Mini PC Debian installation

The Mini PC needs an active internet connection via ethernet when installing Linux.
If such is not easily available, you can use a Windows laptop to share internet via ethernet.

- Step 1: Make sure the Windows laptop is connected to the internet via WiFi.
- Step 2: Go to Settings > Network & Internet > Change adapter options > Right click Wi-Fi > Properties > Sharing > Check "Allow other networks to connect..."
- Step 3: Connect the Mini PC and the laptop with an ethernet cable.

Restart the Mini PC and boot to BIOS by pression the DEL key. Make USB stick the first boot priority. Save and restart.
Install Debian 10 (Buster) normally, pick SSH server and system utils.

### Mini PC post installation

	su
	apt update
	# add contrib non-free to /etc/apt/sources.list

	apt install firmware-iwlwifi firmware-intel-sound firmware-linux firmware-misc-nonfree intel-microcode i965-va-driver-shaders intel-media-va-driver-non-free mesa-utils mesa-utils-extra firmware-realtek

	apt install sudo
	# add jack ALL=(ALL) ALL to /etc/sudoers
	exit

	sudo apt install xfce4 xfce4-terminal curl
	sudo reboot

	sudo apt install wpasupplicant
	sudo chmod 0600 /etc/network/interfaces

	sudo nano /etc/network/interfaces
	# add the following for wifi
	allow-hotplug wlp1s0
	iface wlp1s0 inet dhcp
		wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

	# for wired connection add
	auto enp2s0
	iface enp2s0 inet static
		address 192.168.0.10/24
	
	sudo reboot

	# callicog-related installation steps
	sudo apt install git

	# autologin, modify /etc/lightdm/lightdm.conf, uncomment and add
	user-session=xfce4
	autologin-user=jack
	autologin-user-timeout=0

	# kill remotely
	ssh -l jack callicog-ip
	ps -A | grep xfce4-terminal # get pid
	kill pid

	# disable screenlocker in Session & Startup

### Client computer installation (macOS)
	
Create the `callicogenv` virtual environment.
Make sure the command `python3` points to Python 3.7.

	python3 -m venv callicogenv
	source callicogenv/bin/activate
	pip install wheel
	python -m pip install --upgrade pip

### How to install/uninstall Homebrew in macOS

	sudo /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall.sh)"
	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
	brew update-reset

### PostgreSQL instructions for macOS

	brew install postgresql
	brew services start postgresql
	createuser --interactive
	pip install numpy psycopg2-binary SQLAlchemy flask flask-cors

### PostgreSQL instructions for Debian Stretch

	sudo apt-get install postgresql postgresql-client
	sudo -u postgres createuser --interactive
	pip install wheel
	pip install --upgrade pip
	pip install numpy psycopg2-binary SQLAlchemy flask flask-cors

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

Create the `callicogenv` virtual environment:

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

