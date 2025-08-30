import time
import hid
import psutil

# ----------------------------
# Configuration
# ----------------------------
VENDOR_ID = 0x3633       # DeepCool Vendor ID
PRODUCT_ID = 0x0001      # AK400 Digital Product ID
SENSOR = "k10temp"       # CPU temperature sensor
SHOW_TEMP = True         # Enable temperature display
SHOW_UTIL = True         # Enable CPU utilization display
INTERVAL = 3             # Update interval in seconds

# ----------------------------
# Helper Functions
# ----------------------------
def get_bar_value(value):
    """Convert numeric value to LED bar segments (1 segment per 10 units)."""
    return (value - 1) // 10 + 1


def get_data(value=0, mode="util"):
    """
    Prepare a 64-byte HID data packet.
    
    Parameters:
        value (int): Numeric value to display
        mode (str): 'util' for CPU usage, 'temp' for temperature, 'start' for init
    """
    base_data = [16] + [0] * 63
    base_data[2] = get_bar_value(value)

    # Set header byte based on mode
    if mode == "util":
        base_data[1] = 76
    elif mode == "start":
        base_data[1] = 170
        return base_data
    elif mode == "temp":
        base_data[1] = 19

    # Place digits into the correct positions
    digits = [int(char) for char in str(value)]
    if len(digits) == 1:
        base_data[5] = digits[0]
    elif len(digits) == 2:
        base_data[4], base_data[5] = digits[0], digits[1]
    elif len(digits) == 3:
        base_data[3], base_data[4], base_data[5] = digits[0], digits[1], digits[2]
    elif len(digits) == 4:
        base_data[3], base_data[4], base_data[5], base_data[6] = digits[0], digits[1], digits[2], digits[3]

    return base_data


def get_cpu_temperature(label="CPU"):
    """Return CPU temperature using psutil, fallback if sensor not found."""
    sensors = psutil.sensors_temperatures()
    for sensor_list in sensors.values():
        for sensor in sensor_list:
            if sensor.label == label:
                return sensor.current
    return 0


def get_temperature():
    """Get temperature from specified sensor or fallback to generic CPU sensor."""
    try:
        temp = round(psutil.sensors_temperatures()[SENSOR][0].current)
    except KeyError:
        print("Sensor does not exist in the system.")
        temp = get_cpu_temperature()
    return get_data(value=temp, mode="temp")


def get_utils():
    """Get CPU utilization as a data packet."""
    cpu_percent = round(psutil.cpu_percent())
    return get_data(value=cpu_percent, mode="util")


# ----------------------------
# Main Execution
# ----------------------------
try:
    # Open HID device
    h = hid.device()
    h.open(VENDOR_ID, PRODUCT_ID)
    h.set_nonblocking(1)

    # Send initialization packet
    h.write(get_data(mode="start"))

    # Main loop: update temperature and/or CPU usage
    while True:
        if SHOW_TEMP:
            h.write(get_temperature())
            time.sleep(INTERVAL)
        if SHOW_UTIL:
            h.write(get_utils())
            time.sleep(INTERVAL)

except IOError as error:
    print(f"HID I/O Error: {error}")
    print(
        "Please check the following:\n"
        "- The AK400 Digital CPU cooler is properly connected via USB.\n"
        "- The VENDOR_ID and PRODUCT_ID in the script match your device.\n"
    )


except KeyboardInterrupt:
    print("\nScript terminated by user (KeyboardInterrupt).")
    print("The AK400 Digital display will stop updating.")


finally:
    # Close HID device safely
    if "h" in locals():
        h.close()
