#!/bin/bash

./createdb.sh
./insertintodb.sh
python main.py $1
