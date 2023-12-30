from scripts.endpoint_reader import EndpointReader
from unittest import TestCase
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EMPTY_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'data', 'empty.yml')
NONEXISTENT_FILE_PATH = 'fakenews'

class TestEndpointReader(TestCase):
    '''Tests for EndpointReader'''
    def test_nonexistent_filepath(self):
        with self.assertRaises(FileNotFoundError) as context:
            EndpointReader.read_endpoints(NONEXISTENT_FILE_PATH)
        self.assertTrue(str(context.exception).startswith('File not found'))

    def test_empty_file(self):
        endpoints = EndpointReader.read_endpoints(EMPTY_FILE_PATH)
        self.assertIsNone(endpoints)

    def test_normal_file(self):
        endpoints = EndpointReader.read_endpoints()
        self.assertIsNotNone(endpoints)
        print(type(endpoints))
