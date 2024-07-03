### How to set up a Raspberry Pi video stream web server

#### Prepare the SD Card with Raspberry Pi Imager
1. **Download and Install Raspberry Pi Imager:**
   - [Download Raspberry Pi Imager](https://www.raspberrypi.org/software/) for your operating system.
   - Install the software following the installation instructions for your OS.

2. **Prepare the SD Card:**
   - Insert the SD card into your computer.
   - Open Raspberry Pi Imager.

3. **Select OS:**
   - Click "Choose OS."
   - Select "Raspberry Pi OS (32-bit)".

4. **Select SD Card:**
   - Click "Choose Storage."
   - Select your SD card from the list.

5. **Configure Advanced Options:**
   - Click the gear icon (⚙️) in the bottom right corner.
   - **Set Hostname:** Enter your desired hostname.
   - **Enable SSH:** Check the box to enable SSH.
   - **Set Username and Password:** Enter your desired username and password.
   - **Configure WiFi:** Enter your SSID and password.
   - **Locale Settings:** Set your country, language, and timezone.

6. **Write the OS:**
   - Click "Write" to start writing the OS to the SD card.
   - Wait for the process to complete and safely eject the SD card.

#### Set Up Hardware
1. **Insert SD Card:**
   - Insert the prepared SD card into the Raspberry Pi Zero W.

2. **Connect the Camera:**
   - **Locate the Camera Connector:** The camera connector is a small, thin slot near the edge of the board.
   - **Open the Connector Lock:** Carefully lift the plastic lock on the connector. Be gentle to avoid breaking it.
   - **Insert the Camera Ribbon Cable:** Insert the cable with the metal contacts facing away from the HDMI port.
   - **Close the Connector Lock:** Gently press down the plastic lock to secure the cable in place.

2. **Connect Peripherals (skip if using ssh for remaining steps):**
   - Connect a micro USB power supply.
   - Connect a micro USB adapter for keyboard/mouse.
   - Connect a mini HDMI cable for a display.

3. **Power On:**
   - Connect the power supply to the Raspberry Pi Zero W to power it on.

#### Log On to the Raspberry Pi
1. **Find the IP Address:**
   - Obtain the IP address of the Pi. It should have connected to the wifi network automatically on boot.

2. **SSH into the Raspberry Pi:**
   - Open a terminal on your computer.
   - Use the following command to SSH into your Raspberry Pi:
     ```sh
     ssh <user>@raspberrypi.local
     ```
   - Replace <user> with your username and `raspberrypi.local` with your Pi’s hostname or IP address

#### Install RPiCam Software
1. **Update the System:**
   ```sh
   sudo apt update
   sudo apt upgrade -y
   ```

2. **Install Git:**
   ```sh
   sudo apt install git -y
   ```

3. **Clone the RPiCam Repository:**
   - Go to the [RPiCam GitHub repository](https://github.com/silvanmelchior/RPi_Cam_Web_Interface).
   - Follow the install instructions provided in the repository.
  3. **Clone the RPiCam Repository:**
   ```sh
   git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface
   cd RPi_Cam_Web_Interface
   ./install.sh
   ```

4. **Reboot the Raspberry Pi:**
   ```sh
   sudo reboot
   ```

   - Note: The first reboot will take longer than usual as the repository configures itself.

#### Testing the Camera Web Stream
1. **Wait for the Pi to Reboot:**
   - After the initial reboot, wait for the system to fully start. This may take several minutes.

2. **Access the Camera Stream:**
   - Open a web browser on another machine connected to the same network.
   - Enter the following URL, replacing `raspberrypi.local` with your Pi’s hostname or IP address:
     ```sh
     http://raspberrypi.local/html/
     ```
   - You should see the live stream from the Raspberry Pi camera.
