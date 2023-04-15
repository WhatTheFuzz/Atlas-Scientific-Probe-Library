from atlasscientific.ftdi.atlasdevice import AtlasDevice
from time import sleep
from enum import Enum
import re

class PH_Commands(Enum):
    READ: str = 'r'

class PHProbe(AtlasDevice):

    def __init__(self, device_id: str) -> None:
        super().__init__(device_id=device_id)

    def wait(self) -> None:
        sleep(1)

    def read_ph(self) -> float:
        '''Sends a command to read the pH and waits for the response.
        Returns a floating point number of the detected pH.
        '''
        self.flush()
        # Send the 'r' command for a single read.
        self.send_cmd(PH_Commands.READ.value)
        # Wait the appropriate amount of time.
        self.wait()
        # Read the line.
        line: str = self.read_line()
        self.flush()
        try:
            return float(line)
        except ValueError as e:
            print(f'[-] Failed to read pH, got string {line}; expected float.')

    
    def set_baud(self, rate: int=9600) -> bool:
        '''Change the baud rate of the device.'''
        pass

    def get_baud(self) -> int:
        self.flush()
        self.send_cmd('baud,?')
        self.wait()
        line = self.read_line()
        try:
            baud = re.search(r'\d+', line).group(0)
            return baud
        except IndexError:
            raise ValueError("Unable to get baud, expected int, got {line}")

if __name__ == '__main__':
    ph: PHProbe = PHProbe(device_id="DK0G4FXK")
    print(ph.get_baud())
