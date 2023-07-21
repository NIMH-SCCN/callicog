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
		
		cp ~/callicog/scripts/broadcastIP_slack.sh ~
		cp ~/callicog/scripts/start_callicog_server.sh ~
		cp ~/callicog/scripts/changeres.sh ~
		cp ~/callicog/scripts/flush.sh ~
		cp ~/callicog/scripts/kill_callicog.sh ~
		cp ~/callicog/scripts/start_vncserver.sh ~

10. Disable screenlocker in 'Session & Startup' setting.

11. Install CalliCog.

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

	Download the `wxPython` package from [here](https://drive.google.com/file/d/1sSObbJR2PSWKPJ76bHksWlHL9MY3J2xJ/view?usp=sharing). Put it in the HOME directory.
		
		pip install ~/wxPython-4.1.1-cp37-cp37m-linux_x86_64.whl

12. Make the mini PC broadcast its eduroam IP address to the Slack [channel](https://marmobox.slack.com).

		sudo systemctl edit --force --full broadcast_ip.service

	Add the following lines:

		[Unit]
		Description=Broadcast IP to Slack service
		Wants=network-online.target
		After=network-online.target
		[Service]
		Type=simple
		User=jack
		WorkingDirectory=/home/jack
		ExecStart=/home/jack/broadcastIP_slack.sh
		RestartSec=30
		Restart=on-failure
		[Install]
		WantedBy=multi-user.target

	Save and exit the file.

		sudo systemctl enable broadcast_ip.service
		sudo systemctl start broadcast_ip.service
		sudo systemctl reboot

	The Slack message contains the username `Callicog (192.168.0.20)` by default. Change it accordingly by modifying the `broadcastIP_slack.sh` file.

		nano ~/broadcastIP_slack.sh

	Change the `username` value in the payload.

13. Make Callicog launch on startup.

		mkdir ~/.config/autostart
		cp ~/callicog/installation/callicog.desktop ~/.config/autostart

14. You can also add a CalliCog shortcut to the desktop bottom panel.

15. Make the mini PC stream with VNC. Install the server.

		sudo apt install x11vnc

	Change the IP address in the file `~/start_vncserver.sh`. The first IP is the static Ethernet IP of the mini PC. The second is the CalliCog client (e.g. iMac).

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

### Writing new tasks

Tasks are Python files that contain the instructions for trial-based stimuli presentation. New files are created in `~/callicog/tasks`. Make sure the filename is also added in the database (via 'Tasks' in the web app) without the extension `.py`.

This is the task file skeleton. Copy and paste to start with a new task.

```
from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
	def __init__(self):
		super().__init__()
		self.init_parameters()

	def init_parameters(self):
		pass

	def generate_trials(self):
		pass

	def build_trial(self, trial_parameters={}):
		return []
```

#### The function `init_parameters()`

Used to define general purpose parameters. If task trials do not use parameters, simply return `pass`.
Alternatively, trials can use parameters to vary the presentation of stimuli. For example, if we want trials to show a target stimulus from a  list, the function `init_parameters()` will contain:

```
red_square = Stimulus(shape=StimulusShape.SQUARE,
			size=(100, 100),
			color=(1, 0, 0))
blue_circle = Stimulus(shape=StimulusShape.CIRCLE,
			size=(100, 100),
			color=(0, 0, 1))
stimuli_list = [red_square, blue_circle]

self.add_parameter(Parameter.TARGET, stimuli_list)
```

By default, the parameter added is **pseudorandom**, meaning that trials will be generated depending on all the possible combinations of the added parameters. For instance if we add a delay parameter:

```
delays_list = [1, 2, 4]
self.add_parameter(Parameter.DELAY, delays_list)
```

The task will generate trials for all combinations of `TARGET` and `DELAY`. If you do not want to use a parameter for the generation of trials, simply indicate `pseudorandom=False` when calling the function `self.add_parameter()`. For example:

```
self.add_parameter(Parameter.DELAY, delays_list, pseudorandom=False)
```

Hence, the trials will only be generated from shuffling `stimuli_list`.

The function `init_parameters()` does not return a value. Simply finish the function with `self.add_parameter()` calls or `pass` if the task is static.

#### The function `generate_trials()`

If the task does not have parameters, simply place `pass`. Otherwise, this function is in charge of generating the trials based on the combinations of pseudorandom parameters. If that is the case, just write

```
self.trials = self.pseudorandomize_parameters()
```

There are instances where parameters depend on others. For example, we add the parameter `Parameter.TARGET_NUMBER` which controls the number of stimuli in the trial. If we also want to pseudorandomize the positions of those targets, the number of parameters per trial will be dynamic, making it difficult to calculate the combinations.

For such scenarios, you can modify `self.trials` as you see fit after calling `self.pseudorandomize_parameters()`. The task `supertask_min` does this by going through all generated trials and appending pseudorandom positions based on the number of targets.

However, if no post-processing of trials is necessary, no further code is required.

#### The function `build_trial(trial_parameters={})`

This function returns a list of windows for the current trial. Windows are designed by placing stimuli and controlling the presentation via the use of parameters.
If your task has pseudorandom parameters, the values will be stored in the `trial_parameters` variable. For example, you can access which target to show in the trial by using `trial_parameters[Parameter.TARGET]`.

```
w1 = Window(transition=WindowTransition.RELEASE, label='encoding')
w1_stim = copy.copy(trial_parameters[Parameter.TARGET])
w1_stim.position = (random.randint(-615, 615), random.randint(-335, 335))
w1.add_stimulus(w1_stim)
```

Remember to `copy.copy()` all stimulus variables when adding them to windows.
Window objects can have the following user-defined parameters:

- `transition` (default=`None`). Controls whether to trigger the next window with a touch or release. Possible values: `WindowTransition.RELEASE` and `WindowTransition.TOUCH`.
- `blank` (default=`0`). Defines the duration (in seconds) of a blank window.
- `is_outcome` (default=`False`). Defines the outcome window that will trigger the reward system. It will need stimuli with pre defined outcomes (success, fail or null).
- `timeout` (default=`0`). Duration (in seconds) for the window timeout. The value `0` is symbolic, it will never timeout.
- `is_outside_fail` (default=`False`). Flag that instructs the window to mark the trial as fail if touched anything but stimuli.
- `label` (default=`''`). Window description in terms of behavioral phases (e.g. 'encoding', 'outcome', etc). It can also be used as a custom field (string) to associate any information with the current window.

In addition, stimulus can be static and not retrieved from a parameter list. For example:

```
w2 = Window(transition=WindowTransition.RELEASE)
w2_square = Stimulus(shape=StimulusShape.SQUARE,
			size=(100, 100),
			color=(-1, -1, -1),
			position=(0, 0))
w2.add_stimulus(w1_square)
```

Stimulus objects can have the following user-defined parameters:

- `shape`. Must be a member of `StimulusShape`. The values are defined in the file `task_builder.py` and more can be added.
- `size`. Must be a tuple of two elements (e.g. (100, 100)). Refers to the width and height (in pixels) of the stimuli. PsychoPy automatically adjusts depending on the geometry (e.g. circle taking 100 as its radius).
- `size_touch` (default `None`). Controls the size of the touch area for the stimulus. Also a tuple of two elements.
- `position` (default `None`). Stimulus coordinates (in pixels). PsychoPy considers the center of the screen as (0, 0). Also a tuple of two elements.
- `outcome` (default `None`). Assigns the outcome of the trial to the stimulus. Values are: `Outcome.SUCCESS`, `Outcome.FAIL` and `Outcome.NULL`.
- `color` (default `None`). RGB tuple (e.g. (0,0,1) for blue). -1 refers to black. Check 'RGB color space' [here](https://www.psychopy.org/general/colours.html) for more info.
- `image` (default `None`). Relative path (string) to an image file if the stimulus is an image. For example, a value can be `'tasks/images/composite4-1.jpg'`.
- `auto_draw` (default `False`). If `True`, the stimulus will appear even if it has not been explicitly drawn. Useful for the `hide` functionality.
- `after_touch` (default `[]`). A list of objects like `{'name': 'FUNC'}`. `FUNC` will be executed after touching (or releasing, depending on transition) the stimulus. `FUNC` must be referenced in the `Stimulus` class, function `on_touch`, and also be implemented accordingly.
- `timeout_gain` (default `0`). Adds the number of specified seconds to the window timeout value when the stimulus is touched (or released, depending on transition).

Remember that the function `build_trial()` returns a list of windows (e.g. `return [w1, w2]`).

#### Other useful function: `randomize_from()`

As the name suggests, it randomizes from a list. The function parameters are:

- `sample`. List of values to randomize from.
- `exclude` (default `[]`). List of values to exclude from `sample`.
- `size` (default `0`). Number of random values to get. The value `0` is symbolic, by default the function returns any number of values.

Most importantly, the return value is a list by default, even if only one random value is returned. You will then have to index `[0]` in order to retrieve the value.
Normally, one would randomize from a list of parameters that are not pseudorandom, but it can be any list. In order to access any parameter list previously defined in the task you write

```
self.pseudorandom_parameters[Parameter.PARAMETER_NAME]['values']
```

Always use the string `values` to get the list. The variable `self.pseudorandom_parameters` also contains parameters that are not pseudorandom so ignore the poor choice of name.

Putting things together, assume we want to put random distractors in a window that contains a target. Obviously, we do not want the target to be repeated as a distractor. We also want to randomize the positions of those distractors. Assuming the following parameters: `Parameter.TARGET` and `Parameter.POSITION`, and a `window` object, the distractors are

```
distractors = self.randomize_from(self.pseudorandom_parameters[Parameter.TARGET]['values'], exclude=[trial_parameters[Parameter.TARGET]])
distractor_positions = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]], size=len(distractors))

for i in range(len(distractors)):
	distractor_stim = copy.copy(distractors[i])
	distractor_stim.position = distractor_positions[i]
	distractor_stim.outcome = Outcome.FAIL
	window.add_stimulus(distractor_stim)
```

Distractors are randomized from the list of targets (`self.pseudorandom_parameters[Parameter.TARGET]['values']`), excluding the current target for the trial (`trial_parameters[Parameter.TARGET]`). Since `exclude` must be a list, the stimulus is placed in brackets.
The positions are randomized from the list of positions (`self.pseudorandom_parameters[Parameter.POSITION]['values']`), excluding the current target position (`trial_parameters[Parameter.POSITION]`), again placed in brackets because is just one value and `exclude` must be a list.
In this case, we want to match the number of random positions with the number of distractors, hence `size=len(distractors)`.
Finally, we iterate through the list of distractors to add them to the current window object.


### Raspberry Pi Camera Setup

We use Raspberry Pi Zero W with Raspberry Pi Camera Module v2.1 and the [RPi Cam Web Interface](https://github.com/silvanmelchior/RPi_Cam_Web_Interface) for video stream monitoring of behavior in the CalliCogs. Here are instructions for setting this up:

1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Insert your microSD card into a card reader, plug into your computer
3. Launch Raspberry Pi Imager
	a. Select operating system (e.g. Raspberry Pi OS (32-bit))
	b. Select Storage (your microSD card) e.g. "Generic SD/MMC Media"
	c. Click the gear icon to edit settings (click "No" if asked to use Keychain)
	d. Set hostname following our naming convention, e.g. "pi02a", "pi02b", "pi03a"...
	e. Check to "Enable SSH", and "Use password authentication"
	f. Set username and password to "sccn" and "marmoset"
	g. Check "Configure wireless LAN"
	h. Set SSID to "squirtle" and password to "marmomarm"
	i. Set "Wireless LAN country" to "US"
	j. Check "Set locale settings", set to "America/New York" and "US" keyboard layout
	k. Other settings can be ignored; click "Save"
6. Click "Write" and confirm OK to overwrite the microSD contents; this step will take ~5-10 minutes
7. In Finder, eject the microSD volume
8. Remove the microSD card from the Mac
9. Insert the microSD card into a Raspberry Pi, then plug the Pi into power (it will then auto-attempt to connect to wifi)
10. Ensure that the router hosting the "squirtle" network is online
11. Connect the Mac to the "squirtle" network (pre-shared key, i.e. password, is "marmomarm")
12. In a browser, go to the router admin console webpage (e.g. tplinkwifi.net or 192.168.0.1, user/pw "admin"/"admin")
13. View the connected wireless devices; verify that the Pi with the new hostname is on the network
14. Log in to the Pi from the Mac via ssh: `ssh sccn@<newhostname>.local`
    a. Type "yes" to confirm
    b. Enter the password "marmoset" for the "sccn" user
    c. Verify that you're logged in to the new host, you should see the command prompt change to "sccn@<newhostname>"
15. Type "exit" to quit ssh
16. Use command `ssh-copy-id -i ~/.ssh/id_rsa.pub sccn@<newhostname>.local` to copy the Mac's ssh public key to <newhostname>
    a. Enter the password for "sccn@<newhostname>.local"
    b. Confirm the command executed successfully
    c. Now log in again via ssh: `ssh sccn@<newhostname>.local`
    d. Confirm that no password was required (you logged in using public/private key pair authentication)
17. Next, we need to setup the camera module and the RPi Cam software (based on https://elinux.org/RPi-Cam-Web-Interface)
18. Enter RPi configuration: `sudo raspi-config`
19. Enable the camera interface
    a. Select "3 Interface Options", press Return
    b. Select "I1 Legacy Camera", press Return
    c. Select "Yes" to enable legacy camera support
    d. Select "Ok"
    e. Select "Finish" and press Return
    f. Select "Yes" to reboot now (NOTE: this is necessary!)
20. Update the Raspberry Pi (this will take several minutes):
    ```
    sudo apt-get update
    sudo apt-get dist-upgrade
    sudo apt-get install git
    ```
21. Clone the RPi Cam repository and navigate to the repo:
    ```
    git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git
    cd RPi_Cam_Web_Interface
    ```
22. Install the software: `./install.sh` (this will take several minutes)
    * The default config should be ok, so pres Tab and select "Ok", then hit Return
23. 


### Miscellaneous Observations

#### Errors and exceptions

##### No such file or directory: '/dev/ttyACM0'

Example:
```
sccn@MH02001980MDI ~ % ./callicog.sh 192.168.0.101 run seymour training
{
  "success": 1,
  "body": {
    "data": {
      "status": "[Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such
file or directory: '/dev/ttyACM0'"
    }
  }
}
```

Check whether the pump/sound controller USB cable is plugged in. If it is
plugged into a USB splitter, remove it from the splitter and plug it in
directly.

