# CalliCog

Open-source tools for automated behavioral training and testing, designed for the homecage environment.


## Summary ##

CalliCog is an automated platform for behavioral experiments, designed for the homecage-based **cog**nitive training of common marmosets (_**Calli**thrix jacchus_) and other small nonhuman primates. It delivers behavioral tasks via touchscreens in custom-built operant chambers made from inexpensive and publicly available materials. CalliCog runs on open-source code based in Python, and includes a custom webapp for running experiments and recording behavioral data. 

**Build your own CalliCog setup!** See a full inventory of materials and instructions [here](https://www.doi.org/10.6084/m9.figshare.27873153).

**If you use CalliCog, please cite the [paper]():**\
Scott, J.T., Mendivez Vasquez, B.L., Stewart, B.J., Panacheril, D., Rajit, D.K., Fan, A.Y., Bourne, J.A. (2024) CalliCog: an open-source cognitive neuroscience toolkit for freely behaving nonhuman primates. _bioRxiv_.  

✉️ **Further info or support:** callicog_support@mail.nih.gov 

## Hardware Requirements
CalliCog uses a central computer (**Executive PC**) that controls the operations of up to several (at least one) operant chambers, each controlled by its own computer (**Agent PC**). Operant chambers also contain a **Reward Module** for the delivery of liquid reward, and a **Camera Module** for surveillance. See [inventory](https://www.doi.org/10.6084/m9.figshare.27873153) for full details.

**For software installation, the following hardware is required:** 
* Computer running MacOS (Executive PC). _Recommended: M2 Mac Mini (Apple)._
* Mini PC running Ubuntu (Agent PC). _Recommended: NUC 13 (Intel)._
* Arduino microcontroller (Reward Module). _Recommended: Uno Rev3_
* Raspberry Pi microcomputer (Camera Module). _Recommended: Raspberry Pi Zero W._

## Installation
* [Install Executive PC (Mac)](docs/install_executive_pc.md)
* [Install Agent PC (Mini PC)](docs/install_agent_pc.md)
* [Install Camera Module (Raspberry Pi)](docs/install_camera_module.md)

To install the Reward Module, simply upload [this code](src/arduino/pump_code/pump_code.ino) to the Arduino using [Arduino IDE](https://www.arduino.cc/en/software).

## Running CalliCog

### Initialise the database

The CalliCog database as repository for both collected experimental data and experimental designs. It must be initialised prior to sending commands to operant chambers, or accessing data via the web app.
To initialise the database, open a terminal on the Executive PC, navigate to the `callicog` directory, and enter:
```sh
source .venv/bin/activate
callicog start webapp
```

### Run the web app
The web app acts as the interface to the database. It allows the user to perform [experimental design](docs/experimental_design.md) and to [access experimental data.](docs/data_reporting.md) Follow these links for more details.

To access the webapp:
* Ensure the database is initialised
* Open your favorite web brower (e.g. Google Chrome)
* Navigate to `http://localhost:5000`

### Run an experiment
All subsequent steps first require the Executive PC to first be connected to an active operant chamber (Agent PC) via wired LAN.
Operant chamber Agent PCs automatically run a 'listener' script on boot, and await commands from an Executive PC. Therefore, the user controls experiments directly from the Executive PC.

To begin, open a new terminal on the Executive PC, navigate to the `callicog` directory, and activate the virtual environment:
```sh
source .venv/bin/activate
```
**To run a NEW experiment:**
```sh
callicog run <animal> <hostname>.local <template>

# <animal> = the name of the test subject. Must be first added to the database via the webapp tab 'Animals'.
# <hostname> = your operant chamber hostname.
# <template> = a template for the experiment of choice. Must be first added to the database via the webapp tab 'Templates'.

```
**To resume an EXISTING experiment:**
```sh
callicog resume <hostname>.local <experiment_id>

# <experiment_id> = ID of the experiment. Must be listed in the database under the webapp tab 'Experiments'
```

For help, run `callicog --help`

> [!IMPORTANT]
> CalliCog can run multiple operant chambers simultaneously, but only one operant chamber can be controlled at a time via a terminal. To send a command to a new operant chamber, open up a new terminal.
 
### Monitor an experiment

**For video surveillance:**

If an active operant chamber contains a Camera Module, live video will be streamed by default over a configured wifi network. To access the video stream:
* Ensure the Executive PC is connected to the same network.
* Open a web browser and navigate to http://raspberrypi.local/html/ (replacing 'raspberrypi' with your Raspberry Pi's hostname). See [here](docs/install_camera_module.md) for more info.

**For touchscreen mirroring:**

Operant chambers are configured as VNC servers, meaning that the display can be remotely viewed during real time experimentation. To view a screen mirror:
* Open a VNC client, e.g. [RealVNC Viewer for MacOS](https://www.realvnc.com/en/connect/download/viewer/macos).
* Enter the IP address or hostname (<hostname>.local) to view the screen mirror.
