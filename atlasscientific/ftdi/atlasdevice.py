'''A generic Atlas Scientific device class that uses pylibftdi to communicate
with the sensor. This file is not meant to be used directly, but rather to act
as the superclass that other, more specific sensor classes inherit from.
'''

import os
from time import sleep
from pylibftdi.device import Device
from pylibftdi.driver import FtdiError
from pylibftdi import Driver

class AtlasDevice(Device):
    '''A generic Atlas Scientific device.'''

    def __init__(self, device_id: str) -> None:
        super().__init__(mode='t', device_id=device_id)
        self.device_id = device_id
        self.wait_time = 1.0 # Response time of the device, in seconds.


    def wait(self) -> None:
        '''Wait for the recommended reading delay for the sensor.'''
        sleep(self.wait_time)

    def read_line(self, size=0):
        """
        libftdi uses os.linesep to determine line boundaries; we can change it
        and call this class' super method.
        """
        os.linesep = '\r'
        return self.readline(size=size)

    def read_lines(self):
        """
        libftdi uses os.linesep to determine line boundaries; we can change it
        and call this class' super method.
        """
        os.linesep = '\r'
        return self.readlines()

    def send_cmd(self, cmd: str) -> int:
        """
        Send command to the Atlas Sensor.
        Before sending, add Carriage Return at the end of the command.
        Returns the number of bytes written.
        """
        # Flush the buffer before sending.
        self.flush()
        buf = cmd + '\r'        # add carriage return
        try:
            num_bytes_written = self.write(data=buf)
            self.wait()
            return num_bytes_written
        except FtdiError:
            print("Failed to send command to the sensor.")
            return 0

def get_ftdi_device_list():
    """
    return a list of lines, each a colon-separated
    vendor:product:serial summary of detected devices
    """
    dev_list = []
    for device in Driver().list_devices():
        _, _, serial = device
        dev_list.append(serial)
    return dev_list


if __name__ == '__main__':
    pass
