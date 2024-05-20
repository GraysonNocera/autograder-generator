#!/usr/bin/env bash
apt-get install gcc
apt-get install -y valgrind
apt-get install -y python3.11 python3-pip python3-dev
python3.11 -m pip install -r /autograder/source/requirements.txt