#!/bin/bash

# Stop and disable AK400 services
sudo systemctl stop deepcool-ak400-digital.service
sudo systemctl disable deepcool-ak400-digital.service

sudo systemctl stop deepcool-ak400-digital-restart.service
sudo systemctl disable deepcool-ak400-digital-restart.service

# Remove service files
sudo rm -f /lib/systemd/system/deepcool-ak400-digital.service
sudo rm -f /lib/systemd/system/deepcool-ak400-digital-restart.service

# Reload systemd daemon
sudo systemctl daemon-reload

echo "DeepCool AK400 Digital CPU temperature display services have been stopped, disabled, and completely removed from the system."
