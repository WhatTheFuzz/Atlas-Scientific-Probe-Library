import unittest
from atlasscientific.ftdi.phprobe import PHProbe

device_id = 'DK0G4FXK'

class TestPhProbe(unittest.TestCase):
    '''Test the PH Probe'''

    def test_set_baud(self):
        '''Ensure that setting the baud returns True.'''
        with PHProbe(device_id) as probe:
            did_set_baud = probe.set_baud(rate=9600)
            self.assertTrue(did_set_baud, 'Failed to set baud rate.')

    def test_set_baud_fail(self):
        '''set_baud raises an assertion when given an invalid baud.'''
        with PHProbe(device_id) as probe:
            with self.assertRaises(ValueError):
                probe.set_baud(rate=1)

    def test_get_extended_ph_scale(self):
        with PHProbe(device_id) as probe:
            is_extended = probe.is_extended_ph_scale()
            self.assertTrue(isinstance(is_extended, bool))

if __name__ == '__main__':
    unittest.main()
