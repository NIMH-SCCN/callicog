# Raspberry Pi Camera Setup

We use Raspberry Pi Zero W with Raspberry Pi Camera Module v2.1 and the [RPi Cam Web Interface](https://github.com/silvanmelchior/RPi_Cam_Web_Interface) for video stream monitoring of behavior in the CalliCogs. Here are instructions for setting this up:

1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Insert your microSD card into a card reader, plug into your computer
3. Launch Raspberry Pi Imager
   1. Select operating system (e.g. Raspberry Pi OS (32-bit))
   2. Select Storage (your microSD card) e.g. "Generic SD/MMC Media"
   3. Click the gear icon to edit settings (click "No" if asked to use Keychain)
   4. Set hostname following our naming convention, e.g. "pi02a", "pi02b", "pi03a"...
   5. Check to "Enable SSH", and "Use password authentication"
   6. Set username and password to "sccn" and "marmoset"
   7. Check "Configure wireless LAN"
   8. Set SSID to "squirtle" and password to "marmomarm"
   9. Set "Wireless LAN country" to "US"
   10. Check "Set locale settings", set to "America/New York" and "US" keyboard layout
   11. Other settings can be ignored; click "Save"
6. Click "Write" and confirm OK to overwrite the microSD contents; this step will take ~5-10 minutes
7. In Finder, eject the microSD volume
8. Remove the microSD card from the Mac
9. Insert the microSD card into a Raspberry Pi, then plug the Pi into power (it will then auto-attempt to connect to wifi)
10. Ensure that the router hosting the "squirtle" network is online
11. Connect the Mac to the "squirtle" network (pre-shared key, i.e. password, is "marmomarm")
12. In a browser, go to the router admin console webpage (e.g. tplinkwifi.net or 192.168.0.1, user/pw "admin"/"admin")
13. View the connected wireless devices; verify that the Pi with the new hostname is on the network
14. Log in to the Pi from the Mac via ssh: `ssh sccn@<newhostname>.local`
    1. Type "yes" to confirm
    2. Enter the password "marmoset" for the "sccn" user
    3. Verify that you're logged in to the new host, you should see the command prompt change to "sccn@<newhostname>"
15. Type "exit" to quit ssh
16. Use command `ssh-copy-id -i ~/.ssh/id_rsa.pub sccn@<newhostname>.local` to copy the Mac's ssh public key to <newhostname>
    1. Enter the password for "sccn@<newhostname>.local"
    2. Confirm the command executed successfully
    3. Now log in again via ssh: `ssh sccn@<newhostname>.local`
    4. Confirm that no password was required (you logged in using public/private key pair authentication)
17. Next, we need to setup the camera module and the RPi Cam software (based on https://elinux.org/RPi-Cam-Web-Interface)
18. Enter RPi configuration: `sudo raspi-config`
19. Enable the camera interface
    1. Select "3 Interface Options", press Return
    2. Select "I1 Legacy Camera", press Return
    3. Select "Yes" to enable legacy camera support
    4. Select "Ok"
    5. Select "Finish" and press Return
    6. Select "Yes" to reboot now (NOTE: this is necessary!)
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
