from atlasdevice import AtlasDevice
from time import sleep

class PHProbe(AtlasDevice):

    def __init__(self, device_id: str) -> None:
        super().__init__(device_id=device_id)

    def wait(self) -> None:
        sleep(1.3)

    def read_ph(self) -> float:
        '''Sends a command to read the pH and waits for the response.
        Returns a floating point number of the detected pH.
        '''
        # Send the 'r' command for a single read.
        self.send_cmd('r')
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
