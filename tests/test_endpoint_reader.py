from scripts.endpoint_reader import EndpointReader
import unittest
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EMPTY_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'data', 'data/fetch.yml')
NONEXISTENT_FILE_PATH = 'fakenews'

class TestEndpointReader(unittest.TestCase):
    '''Tests for EndpointReader'''
    def test_nonexistent_filepath(self):
        self.assertRaises(OSError, EndpointReader.read_endpoints(NONEXISTENT_FILE_PATH))

    def test_empty_file(self):
        endpoints = EndpointReader.read_endpoints(EMPTY_FILE_PATH)
        self.assertIsNotNone(endpoints)

    def test_normal_file(self):
        endpoints = EndpointReader.read_endpoints()
        self.assertIsNone(endpoints)
