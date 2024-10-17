# CalliCog #

### Server installation (mini PC)

1. Flash USB with Debian 10.11 (Buster) [ISO file](https://drive.google.com/file/d/1hRkasJ1nOOUxclgPgWfXA9Y2jxiqqZsI/view?usp=sharing) using [balenaEtcher](https://www.balena.io/etcher/).

2. The Mini PC needs an active Internet connection via Ethernet when installing Debian. You can use a Windows laptop with WiFi to achieve this.

	- Step 2: Go to Settings > Network & Internet > Change adapter options > Right click Wi-Fi > Properties > Sharing > Check "Allow other networks to connect..."
	- Step 3: Connect the Mini PC and the laptop with an Ethernet cable.

3. Restart the Mini PC and boot to BIOS by pression the DEL key. Make USB stick the first boot priority. Save and restart.
4. Install Debian 10 (Buster) normally, pick SSH server and system utils. Some tips:

	- Use 'Graphical Install'.
	- Say no to 'Detect hardware from removable media'.
	- Pick 'Australia' for location and 'American English' for keyboard layout.
	- Pick a relevant hostname and domain (e.g. `callicog3` and `callicog.net`).
	- When choosing the media destination, select 'Use entire disk' and a drive that is not the USB stick.
	- Choose `ftp.au.debian.org` for the installation mirror.
	- From the software list, pick 'SSH server' and 'standard system utilities' ONLY.

5. Restart and change back the BIOS boot priority. Unplug USB stick.

### Server post-installation

1. Add non-free repositories to Debian.

		su
		apt update
		nano /etc/apt/sources.list

	It should look like this:

		deb http://ftp.au.debian.org/debian/ buster main contrib non-free
		deb-src http://ftp.au.debian.org/debian/ buster main contrib non-free

		deb http://security.debian.org/debian-security buster/updates main contrib non-free
		deb-src http://security.debian.org/debian-security buster/updates main contrib non-free

		deb http://ftp.au.debian.org/debian/ buster-updates main contrib non-free
		deb-src http://ftp.au.debian.org/debian/ buster-updates main contrib non-free

2. Execute the following:

		apt install firmware-iwlwifi firmware-intel-sound firmware-linux firmware-misc-nonfree intel-microcode i965-va-driver-shaders intel-media-va-driver-non-free mesa-utils mesa-utils-extra firmware-realtek

3. Add the line `jack ALL=(ALL) ALL` for user `jack` to sudoers file.

		apt install sudo
		nano /etc/sudoers
		exit

4. Install more packages.

		sudo apt install xfce4 xfce4-terminal xfce4-power-manager curl git
		sudo reboot

5. Clone `callicog `repository.
		
		cd ~
		git clone https://github.com/Bourne-Lab-ARMI/callicog.git

6. Add a WiFi interface. Edit `/etc/network/interfaces`
		
		sudo apt install wpasupplicant
		sudo chmod 0600 /etc/network/interfaces
		sudo nano /etc/network/interfaces

	And add the following:

		allow-hotplug wlp1s0
		iface wlp1s0 inet dhcp
		wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

	For a wired connection add:

		auto enp2s0
		iface enp2s0 inet static
		address 192.168.0.10/24

	Or any other relevant static IP address.

	The file `wpa_supplicant.conf` does not exist yet. Copy it from the repository.

		sudo cp ~/callicog/installation/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf

	Restart.
	
		sudo reboot

7. You should have Internet via WiFi.

8. Configure Debian for autologin. Remember that the file `lightdm.conf` contains instructions for the `jack` user.

		sudo cp ~/callicog/installation/lightdm.conf /etc/lightdm/lightdm.conf

9. Copy useful scripts to the HOME directory.
		
		sudo ln -s ~/callicog/scripts/broadcastIP_slack ~
		sudo ln -s ~/callicog/scripts/start_callicog_server ~
		sudo ln -s ~/callicog/scripts/changeres.sh ~
		sudo ln -s ~/callicog/scripts/flush.sh ~
		sudo ln -s ~/callicog/scripts/kill_callicog.sh ~
		sudo ln -s ~/callicog/scripts/start_vncserver.sh ~

11. Disable screenlocker in 'Session & Startup' setting.

12. Install CalliCog.

		cd ~
		sudo apt install python3-venv python3-pip
		python3.7 -m venv callicogenv
		source callicogenv/bin/activate
		pip install wheel
		python -m pip install --upgrade pip

	Install PsychoPy.

		sudo apt-get install libsdl2-dev
		python -m pip install --upgrade Pillow
		pip install pyserial numpy
		pip install matplotlib
		pip install pyqt5==5.14
		pip install psychopy --no-deps
		pip install pyyaml requests freetype-py pandas python-bidi pyglet json-tricks scipy packaging future imageio


    Install the `wxPython` package. We have to build from source due to Debian and Pyenv:
 https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip/
	
 https://github.com/pyenv/pyenv/wiki#how-to-build-cpython-with---enable-shared
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.11.8


13. Make Callicog launch on startup; create the autostart directory, and then
    symlink the Callicog autostart script into it.

        ```
		mkdir ~/.config/autostart
		ln -s ~/callicog/installation/callicog.desktop ~/.config/autostart
        ```

14. You can also add a CalliCog shortcut to the desktop bottom panel.

15. Make the mini PC stream with VNC. Install the server.

		`sudo apt install x11vnc`

    Create a symlink to the vnc autostart script:

        `ln -s ~/callicog/installation/vnc_autostart.desktop ~/.config/autostart`

    This will launch a bash shell on startup and run: `x11vnc -display :0`,
    which will enable you to connect to VNC into this miniPC from a control
    computer.

16. Disable sleep, hibernate and hybrid-sleep modes:

        `sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target`

### Client installation (macOS)

1. Clone the repository.

		cd ~
		git clone https://github.com/Bourne-Lab-ARMI/callicog.git

2. Copy useful command shortcuts.

		cp ~/callicog/scripts/start_postgresql.sh ~
		cp ~/callicog/scripts/start_webapp.sh ~
		cp ~/callicog/scripts/callicog.sh ~

2. Create a Ptyhon3 virtual environment. Change the command `python3.X` to the Python 3 version installed in macOS.

		python3.X -m venv callicogenv
		source callicogenv/bin/activate
		pip install wheel
		python -m pip install --upgrade pip

3. Deal with Homebrew in macOS :grimacing:

	To uninstall:

		sudo /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall.sh)"

	To install:

		/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
		brew update-reset

4. Install PostgreSQL in macOS.

		brew install postgresql
		brew services start postgresql

	Create a database super user:

		createuser --interactive

	Install dependencies for web app:

		source ~/callicogenv/bin/activate
		pip install numpy psycopg2-binary SQLAlchemy flask flask-cors

	To install in a Debian client:

		sudo apt-get install postgresql postgresql-client
		sudo -u postgres createuser --interactive

5. If the `createuser` command does not work, nor `psql`, you may need to lanch PostgreSQL manually:

		/usr/local/opt/postgresql/bin/postgres -D /usr/local/var/postgres

	A shortcut can be found in the HOME directory:


5. If the `createuser` command does not work, nor `psql`, you may need to lanch PostgreSQL manually:

		/usr/local/opt/postgresql/bin/postgres -D /usr/local/var/postgres

	A shortcut can be found in the HOME directory:

		/usr/local/opt/postgresql/bin/postgres -D /usr/local/var/postgres

	A shortcut can be found in the HOME directory:

		~/start_postgresql.sh

### Run web application

	./start_webapp.sh

### Run CalliCog

To run a NEW experiment:

	cd ~
	./callicog.sh CALLICOG_SERVER_IP run ANIMAL_CODE TEMPLATE_CODE

To resume an ongoing experiment:

	cd ~
	./callicog.sh CALLICOG_SERVER_IP resume EXPERIMENT_ID

Make sure the IP address exists, as well as the animal and template codes. A template is a collection of tasks with custom progression criteria, and can be created in the web app.
