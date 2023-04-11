from atlasscientific.ftdi.atlasdevice import AtlasDevice
from time import sleep
from enum import Enum

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

    
if __name__ == '__main__':
    ph: PHProbe = PHProbe(device_id="DK0G4FXK")
    print(ph.read_ph())
