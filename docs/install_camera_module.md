# Camera Module Installation

## Prepare an SD card with Raspberry Pi Imager

1. Download and Install [Raspberry Pi Imager](https://www.raspberrypi.org/software/).
2. Insert the SD card for the Raspberry Pi into your computer.
3. Open Raspberry Pi Imager.
4. Click "Choose OS" and select "Raspberry Pi OS (32-bit)".
5. Click "Choose Storage" and select your SD card from the list.
6. Configure Advanced Options
   * Click the gear icon (⚙️) in the bottom right corner.
   * **Set Hostname:** Enter your desired hostname.
   * **Enable SSH:** Check the box to enable SSH.
   * **Set Username and Password:** Enter your desired username and password.
   * **Configure WiFi:** Enter your SSID and password.
   * **Locale Settings:** Set your country, language, and timezone.
7. Click "Write" to start writing the OS to the SD card.
8. Once complete, safely eject and insert the prepared SD card into the Raspberry Pi Zero W.

## Install RpiCam Software
1. Connect the Raspberry Pi to a desktop computer via USB.
2. Obtain the IP address of the Pi. It should have connected to your wifi network automatically on boot.
3. Open a terminal on your computer, and remotely access the Raspberry Pi via SSH.
   ```sh
   ssh <user>@raspberrypi.local
   #Replace <user> with your username and `raspberrypi.local` with your Pi’s hostname or IP address
   ```
4. Once connected remotely, update the system.
   ```sh
   sudo apt update
   sudo apt upgrade -y
   ```
5. Install git.
   ```sh
   sudo apt install git -y
   ```
6. Clone the open access [RPiCam GitHub repository](https://github.com/silvanmelchior/RPi_Cam_Web_Interface). Follow the install instructions provided in the repository.
   ```sh
   git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface
   cd RPi_Cam_Web_Interface
   ./install.sh
   ```
7. Reboot the Raspberry Pi.
   ```sh
   sudo reboot
   ```
   Note: The first reboot will take longer than usual as the repository configures itself.

## Test the Camera Module web stream
1. Wait for the Pi to fully reboot.
2. Open a web browser on another machine connected to the same wifi network.
3. Enter the following URL, replacing `raspberrypi.local` with your Pi’s hostname or IP address:
   ```sh
   http://raspberrypi.local/html/
   ```
   You should now see the live stream from the Raspberry Pi camera.


> [!Note]
> Rpi Cam Web Interface is a third-party open access application, and is not supported by CalliCog. Therefore, protocols for its installation and/or operation may change in the future. For complete details on how to operate this application, see the [documentation](https://elinux.org/RPi-Cam-Web-Interface).
