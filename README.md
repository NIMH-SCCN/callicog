# CalliCog

Open-source tools for automated behavioral training and testing, designed for the homecage environment.


## Summary ##

CalliCog is an automated platform for behavioral experimentats, designed for the homecage-based training of common marmosets (_Callithrix jacchus_) and other small nonhuman primates. It delivers behavioral tasks via touchscreens in custom-built operant chambers made from inexpensive and publicly available materials. CalliCog runs on open-source code based in Python, and includes a custom webapp for running experiments and recording behavioral data. 

**Build your own CalliCog setup!** See a full inventory of materials and instructions [here]().

**If you use CalliCog, please cite the [paper]():**\
Scott, J.T., Mendivez Vasquez, B.L., Stewart, B.J., Panacheril, D., Rajit, D.K., Fan, A.Y., Bourne, J.A. (2024) CalliCog: an open-source cognitive neuroscience toolkit for freely behaving nonhuman primates. _bioRxiv_.  

✉️ **Further info or support:** callicog_support@mail.nih.gov 

## Hardware Requirements
CalliCog uses a central computer (**Executive PC**) that controls the operations of up to several (at least one) operant chambers, each controlled by its own computer (**Agent PC**). Operant chambers also contain a **Reward Module** for the delivery of liquid reward, and a **Camera Module** for surveillance. See [inventory]() for more.

**For software installation, the following hardware is required:** 
* Computer running MacOS (Executive PC). _Recommended: M2 Mac Mini (Apple)._
* Mini PC running Ubuntu (Agent PC). _Recommended: NUC 13 (Intel)._
* Arduino microcontroller (Reward Module). _Recommended: Uno Rev3_
* Raspberry Pi microcomputer (Camera Module). _Recommended: Raspberry Pi Zero W._

## Installation
* [Install Executive PC (Mac)](docs/install_executive_pc.md)
* [Install Agent PC (Mini PC)](docs/install_agent_pc.md)
* [Install Camera Module (Raspberry Pi)](docs/install_camera_module.md)

To install the Reward Module (Arduino), simply upload [this code](src/arduino/pump_code/pump_code.ino) to the Arduino using [Arduino IDE](https://www.arduino.cc/en/software).

## Running CalliCog

> Include basic run-through to test without setting up minipc
