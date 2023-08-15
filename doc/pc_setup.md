CalliCog Mini-PC Setup
======================

### Configure hostname

We want to be able to see which devices are connected to the network, and be
able to connect to them without having to remember (or even know!) which IP
they're configured to use. We want to be able to connect like so:

    `ssh sccn@ccpc02` or `ssh sccn@pi02b`

To do this, we must:

    1. Enable the Bonjour protocol
        i. Install Avahi to enable the Bonjour protocol:
            ```
            sudo apt update
            sudo apt install avahi-daemon
            ```
        ii. Configure Avahi:
            - `sudo nano /etc/avahi/avahi-daemon.conf`
            - Under `[server]` add the lines:
                ```
                host-name=<your host name>
                domain-name=local
                ```
            - Save the changes
        iii. Restart Avahi daemon:
            ```
            sudo systemctl restart avahi-daemon
            ```

`/etc/hosts`
