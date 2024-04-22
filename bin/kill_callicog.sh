#!/bin/bash

kill -9 $(pgrep -f marmobox_listener.py) 2> /dev/null
