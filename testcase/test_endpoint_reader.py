from scripts.endpoint_reader import EndpointReader
from unittest import TestCase
from unittest import mock
from unittest.mock import mock_open
import yaml

YML_TEXT = '''
- headers:
    user-agent: fetch-synthetic-monitor
  method: GET
  name: fetch index page
  url: https://fetch.com/
'''
YML_DATA = [{
    'headers' : {'user-agent': 'fetch-synthetic-monitor'},
    'method' : 'GET',
    'name' : 'fetch index page',
    'url' : 'https://fetch.com/',
}]
MOCK_FILE_NOT_FOUND = mock.Mock(side_effect=FileNotFoundError())
MOCK_YAML_ERROR= mock.Mock(side_effect=yaml.YAMLError())

class TestEndpointReader(TestCase):
    '''Tests for EndpointReader'''

    @mock.patch('builtins.open', mock_open(mock=MOCK_FILE_NOT_FOUND))
    def test_read_endpoints_notfound(self):
        endpoints = EndpointReader.read_endpoints('nonexistentfile.yml')
        self.assertIsNone(endpoints)

    @mock.patch('builtins.open', mock_open(mock=MOCK_YAML_ERROR))
    def test_read_endpoints_yamlerror(self):
        endpoints = EndpointReader.read_endpoints('billy.xml')
        self.assertIsNone(endpoints)

    @mock.patch('builtins.open', mock_open())
    def test_read_endpoints_empty(self):
        endpoints = EndpointReader.read_endpoints('emptyfile.yml')
        self.assertIsNone(endpoints)

    @mock.patch('builtins.open', mock_open(read_data=YML_TEXT))
    def test_read_endpoints_normal(self):
        endpoints = EndpointReader.read_endpoints('normalfile.yml')
        self.assertIsNotNone(endpoints)
        self.assertEquals(endpoints, YML_DATA)
