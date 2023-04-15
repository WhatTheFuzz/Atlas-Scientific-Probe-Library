import string

import pylibftdi
from pylibftdi.device import Device
from pylibftdi.driver import FtdiError
from pylibftdi import Driver
import os
import time

class AtlasDevice(Device):

    def __init__(self, device_id: str) -> None:
        super().__init__(mode='t', device_id=device_id)
        self.device_id = device_id
        self.wait_time = 1.0 # Response time of the device, in seconds.


    def wait(self) -> None:
        sleep(self.wait_time)

    def read_line(self, size=0):
        """
        libftdi uses os.linesep to determine line boundaries; we can change it
        and call this class' super method.
        """
        os.linesep = '\r'
        return self.readline()

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
        vendor, product, serial = device
        dev_list.append(serial)
    return dev_list


def main():

    real_raw_input = vars(__builtins__).get('raw_input', input) # used to find the correct function for python2/3

    print("\nWelcome to the Atlas Scientific Raspberry Pi FTDI Serial example.\n")
    print("    Any commands entered are passed to the board via UART except:")
    print("    Poll,xx.x command continuously polls the board every xx.x seconds")
    print("    Pressing ctrl-c will stop the polling\n")
    print("    Press enter to receive all data in buffer (for continuous mode) \n")
    print("Discovered FTDI serial numbers:")

    devices = get_ftdi_device_list()
    cnt_all = len(devices)
    
    #print "\nIndex:\tSerial: "
    for i in range(cnt_all):
        print(  "\nIndex: ", i, " Serial: ", devices[i])
    print( "===================================")

    index = 0
    while True:
        index = real_raw_input("Please select a device index: ")

        try:
            dev = AtlasDevice(devices[int(index)])
            break
        except pylibftdi.FtdiError as e:
            print( "Error, ", e)
            print( "Please input a valid index")

    print( "")
    print(">> Opened device ", devices[int(index)])
    print(">> Any commands entered are passed to the board via FTDI:")

    time.sleep(1)
    dev.flush()
    
    
    while True:
        input_val = real_raw_input("Enter command: ")

        
        
        # continuous polling command automatically polls the board
        if input_val.upper().startswith("POLL"):
            delaytime = float(string.split(input_val, ',')[1])
            
            dev.send_cmd("C,0") # turn off continuous mode
            #clear all previous data
            time.sleep(1)
            dev.flush()
            
            # get the information of the board you're polling
            print("Polling sensor every %0.2f seconds, press ctrl-c to stop polling" % delaytime)
    
            try:
                while True:
                    dev.send_cmd("R")
                    lines = dev.read_lines()
                    for i in range(len(lines)):
                        # print lines[i]
                        if lines[i][0] != '*':
                            print("Response: " , lines[i])
                    time.sleep(delaytime)
    
            except KeyboardInterrupt:       # catches the ctrl-c command, which breaks the loop above
                print("Continuous polling stopped")

        else:
            # pass commands straight to board
            if len(input_val) == 0:
                lines = dev.read_lines()
                for i in range(len(lines)):
                    print( lines[i])
            else:
                dev.send_cmd(input_val)
                time.sleep(1.3)
                lines = dev.read_lines()
                for i in range(len(lines)):
                    print( lines[i])

if __name__ == '__main__':
    pass
