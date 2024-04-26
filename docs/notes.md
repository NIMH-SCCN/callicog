### Miscellaneous Observations

#### Development

##### Mocking the USB reward module device
In order to mock a reward module connected via USB at `/dev/ttyACM0`, which is
expected by the Callicog listener, do:

0. Open a terminal running on the Callicog, via SSH, VNC or directly
1. `sudo socat -d -d pty,raw,echo=1,link=/dev/ttyACM0 -`
2. Press `Ctrl-z` to suspend the job
3. `sudo chmod a+rw /dev/ttyACM0`

Step 1. creates a mock device on the appropriate USB port which listens for
input and echos it to stdout, so it appears in the terminal window; step 2.
suspends this job and returns you to the command prompt; step 3. grants
sufficient read/write permissions to the USB device so that the Callicog
process can communicate to it.

Now, keep this SSH session or terminal window open, and if the listener is
running you can initiate tasks and have it run.

#### Errors and exceptions

##### No such file or directory: '/dev/ttyACM0'

Example:
```
sccn@MH02001980MDI ~ % ./callicog.sh 192.168.0.101 run seymour training
{
  "success": 1,
  "body": {
    "data": {
