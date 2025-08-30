#!/bin/bash

# Install Dependencies

sudo apt update
sudo apt install python3-dev libhidapi-dev libhidapi-hidraw0

# Install Deepcool AK400 Python script and enable services

sudo cp -f deepcool-ak400-digital.service /lib/systemd/system/
sudo cp -f deepcool-ak400-digital-restart.service /lib/systemd/system/
sudo cp -f deepcool-ak400-digital.py /usr/bin/deepcool-ak400-digital.py

sudo systemctl enable deepcool-ak400-digital.service
sudo systemctl enable deepcool-ak400-digital-restart.service
sudo systemctl start deepcool-ak400-digital.service

echo "DeepCool AK400 Digital CPU temperature display services have been successfully installed and started."