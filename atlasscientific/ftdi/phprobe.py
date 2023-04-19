'''A class representing the Atlas Scientific pH probe.'''

import re
from atlasscientific.ftdi.atlasdevice import AtlasDevice


class PHProbe(AtlasDevice):
    '''Stubs out the Atlas Scientific pH probe.'''

    def __init__(self, device_id: str) -> None:
        super().__init__(device_id=device_id)

    def read_ph(self) -> float:
        '''Sends a command to read the pH and waits for the response.
        Returns a floating point number of the detected pH.
        '''
        # Send the 'r' command for a single read.
        self.send_cmd('r')
        # Read the line.
        line: str = self.read_line()
        try:
            return float(line)
        except ValueError as err:
            raise ValueError(f'[-] Failed to read pH, got string {line}; ' \
                             f'expected float.') from err


    def set_baud(self, rate: int=9600) -> bool:
        '''Change the baud rate of the device.'''
        pass

    def get_baud(self) -> int:
        '''Get the current baud rate of the device.'''
        self.flush()
        self.send_cmd('baud,?')
        line = self.read_line()
        try:
            baud = re.search(r'\d+', line).group(0)
            return baud
        except IndexError as err:
            raise ValueError(f'Unable to get baud, expected int, ' \
                             f'got {line}') from err

if __name__ == '__main__':
    ph: PHProbe = PHProbe(device_id='DK0G4FXK')
    print(ph.get_baud())
