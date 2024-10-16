# CalliCog

Open-source tools for automated behavioral training and testing, designed for the homecage environment.


## Summary ##

CalliCog is an automated platform for behavioral experimentation designed for homecage-based training of common marmosets (_Callithrix jacchus_) and other small nonhuman primates. It delivers behavioral tasks via touchscreens in custom-built operant chambers made from inexpensive and publicly available materials. It is powered by open-source code based in Python, and uses a custom webapp for running experiments and recording behavioral data. 

**To build your own CalliCog setup,** see a full inventory of materials and instructions [here]().

**If you use CalliCog, please cite the [paper]():**\
Scott, J.T., Mendivez Vasquez, B.L., Stewart, B.J., Panacheril, D., Rajit, D.K., Fan, A.Y., Bourne, J.A. (2024) CalliCog: an open-source cognitive neuroscience toolkit for freely behaving nonhuman primates. _bioRxiv_.  

✉️ **Further info or support:** callicog_support@mail.nih.gov 

<br>

## Hardware Requirements
CalliCog uses a central computer (**Executive PC**) that controls the operations of up to several (at least one) operant chambers, each controlled by its own computer (**Agent PC**). Operant chambers also contain a **Reward Module** for the delivery of liquid reward, and a **Camera Module** for surveillance. A full inventory of materials, _including part/model no's_, can be found [here]().
<br>

**For software installation, the following hardware is required:** 
* Computer running MacOS (Executive PC):\
_Recommended: M2 Mac Mini (Apple); MacOS Sonoma (v14.5)_ 
* Operant chamber mini PC running Ubuntu (Agent PC)\
_Recommended: NUC 13 (Intel); Ubuntu (v22.04)_ 
* Arduino Uno Rev3 microcontroller (Reward Module):
* Raspberry Pi microcomputer (Camera Module)\
_Recommended: Raspberry Pi Zero W_
<br>

**For Reward Module installation**, upload [this code](src/arduino/pump_code/pump_code.ino) to the Arduino using [Arduino IDE](https://www.arduino.cc/en/software).\
**For Camera Module installation**, see [here](docs/raspberry_pi_camera.md)\
<br>
For all other installations, see below.
> Note to self: check rpi cam doc

<br>

## Installation



## Running CalliCog

> Include basic run-through to test without setting up minipc
