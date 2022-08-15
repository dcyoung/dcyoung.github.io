---
title: "Using hardware sensors in Python: I2C"
date: 2017-08-15T00:00:00-00:00
last_modified_at: 2017-08-15T00:00:00-00:00
categories:
  - electronics
  - diy
permalink: /post-python-i2c-sensor/
classes: wide
toc: true
excerpt: Creating a python library to communicate w/ a hardware sensor on a Raspberry PI.
header:
  og_image: https://media.digikey.com/Photos/AKM%20Semiconductor/MFG_AK9750.jpg
  teaser: https://media.digikey.com/Photos/AKM%20Semiconductor/MFG_AK9750.jpg
---

## Background

For a prototype device, I needed to communicate with a hardware sensor using a Raspberry PI. The sensor used a 16bit digital output to I2C bus. So I created a python library to handle the low level communication... allowing me to write application logic in python. I've outlined the process below, which should apply to many sensors.

To see the complete source code see: [github.com/detectlabs/AK9750-python-library](https://github.com/detectlabs/AK9750-python-library)

## Constants

First, define any necessary constants for your device. This includes any settings, register addresses or parameter values defined in your sensors datasheet. For example, the values below for an AK9750 sensor were sourced from the official [sensor datasheet](https://media.digikey.com/pdf/Data%20Sheets/AKM%20Semiconductor%20Inc.%20PDFs/AK9750_Oct2015.pdf).

```python
I2C_SPEED_STANDARD = 100000
I2C_SPEED_FAST = 400000

AK9750_DEFAULT_ADDRESS = 0x64  # 7-bit unshifted default I2C Address

# Register addresses
AK9750_TMP = 0x0E
AK9750_ECNTL1 = 0x1C
...

# Valid sensor modes - Register ECNTL1
AK9750_MODE_STANDBY = 0b000
...
```

## General IO

Write some utilities to handle general IO over i2c.

```python
I2C_BUS = smbus.SMBus(1)

def i2c_read(address, reg, length):
    """ i2c bus read """
    result = []
    try:
        result = I2C_BUS.read_i2c_block_data(address, reg, length)
    except IOError:
        print "IOError"
        return []

    return result


def i2c_write(address, reg, data):
    """ i2c bus write """
    try:
        I2C_BUS.write_i2c_block_data(address, reg, data)
    except IOError:
        print "IOError"
        return False

    return True


def get_16_bit_int(byte_list):
    """ Returns an int16 intepretation of the first two bytes of a list of bytes """
    return struct.unpack("=h", ''.join([chr(i) for i in byte_list[:2]]))[0]
```

## Sensor API

Create a class to abstract your sensor, and add utility methods to read sensor values or write commands.

```python
class AK9750(object):
    """ AK9750 """

    def __init__(self, address=AK9750_DEFAULT_ADDRESS):
        """ Initialize the AK9750 Sensor """
        self.device_address = address
        print "Device address: ", self.device_address

    def read_register(self, reg):
        """ Reads a byte from the specified register at this device's address """
        return i2c_read(self.device_address, reg, 1)[0]

    def read_register_16(self, reg):
        """ Reads a 16 bit int value from  from the specified register at this device's address """
        return get_16_bit_int(i2c_read(self.device_address, reg, 2))

    def write_register(self, reg, byte):
        """ Writes the byte to the specified register at this device's address """
        i2c_write(self.device_address, reg, [byte])

    def set_to_stanby(self):
        """ An example to set the sensor to standy mode """
        mode = AK9750_MODE_STANDBY

        # Read current settings
        current_settings = self.read_register(AK9750_ECNTL1)

        # Clear the mode bits and replace with the new setting
        current_settings = current_settings & 0b11111000
        current_settings = current_settings | mode

        # Write
        self.write_register(AK9750_ECNTL1, current_settings)

    def get_temperature(self):
        """ An exampleto read data from the sensor...
            Returns the temperature in degrees celcius 
        """
        value = self.read_register_16(AK9750_TMP)
        # Temp is 10-bit
        value = value >> 6
        return 26.75 + (value * 0.125)
    
    ...
```
