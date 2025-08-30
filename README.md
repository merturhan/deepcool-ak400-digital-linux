# DeepCool AK400 Digital CPU Fan Display

Python script and systemd services to display **CPU temperature** and **CPU utilization** on the **DeepCool AK400 Digital CPU cooler**.
The script reads temperature from Linux sensors and updates the AK400 display at a configurable interval.

---

## Features

* Display CPU temperature on AK400 digital display
* Optionally display CPU utilization
* Configurable update interval
* Easy setup and removal via scripts

---

## Configuration

You can configure the following parameters in `deepcool-ak400-digital.py`:

```python
VENDOR_ID = 0x3633       # DeepCool Vendor ID
PRODUCT_ID = 0x0001      # AK400 Digital Product ID
SENSOR = "k10temp"       # CPU temperature sensor
SHOW_TEMP = True         # Enable temperature display
SHOW_UTIL = True         # Enable CPU utilization display
INTERVAL = 3             # Update interval in seconds
```

> Adjust `SENSOR` according to your system’s CPU temperature sensor name:
>
> ```bash
> python3 -c "import psutil; print(psutil.sensors_temperatures())"
> ```

---

## Installation

Run the setup script to install the Python script and systemd services:

```bash
chmod +x setup.sh
./setup.sh
```

This will:

1. Install required dependencies (`python3-dev`, `libhidapi-dev`, `libhidapi-hidraw0`)
2. Copy the Python script and systemd service files to the correct locations
3. Enable and start the services

Check the status of the service:

```bash
systemctl status deepcool-ak400-digital.service
```

---

## Removal

To remove the services and the script from your system:

```bash
chmod +x remove.sh
./remove.sh
```

This will:

1. Stop the services
2. Disable them from startup
3. Remove the systemd service files
4. Optionally remove the Python script (`/usr/bin/deepcool-ak400-digital.py`)

After removal, reload systemd daemon:

```bash
sudo systemctl daemon-reload
sudo systemctl reset-failed
```

---

## Requirements

* Linux system with Python 3
* DeepCool AK400 Digital CPU cooler connected via USB
* Python packages: `hid`, `psutil`
* Systemd (for managing services)

---

## Notes

* Make sure the `PRODUCT_ID` matches your device (for AK400 Digital it is `0x0001`).
* Only temperature display can be enabled/disabled; CPU utilization is optional.
* `INTERVAL` controls how often the display refreshes.

---
