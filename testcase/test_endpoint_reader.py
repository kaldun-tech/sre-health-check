'''Tests for endpoint reader'''
from unittest import TestCase
from unittest import mock
from unittest.mock import mock_open
import yaml
from scripts.endpoint_reader import read_endpoints

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
    '''Tests for endpoint_reader'''

    @mock.patch('builtins.open', mock_open(mock=MOCK_FILE_NOT_FOUND))
    def test_read_endpoints_nonexistent(self):
        '''Tests read endpoints for nonexistent YAML'''
        endpoints = read_endpoints('nonexistentfile.yml')
        self.assertIsNone(endpoints)

    @mock.patch('builtins.open', mock_open(mock=MOCK_YAML_ERROR))
    def test_read_endpoints_yamlerror(self):
        '''Tests read endpoints for bad YAML file'''
        endpoints = read_endpoints('billy.xml')
        self.assertIsNone(endpoints)

    @mock.patch('builtins.open', mock_open())
    def test_read_endpoints_empty(self):
        '''Tests read endpoints for empty YAML file'''
        endpoints = read_endpoints('emptyfile.yml')
        self.assertIsNone(endpoints)

    @mock.patch('builtins.open', mock_open(read_data=YML_TEXT))
    def test_read_endpoints_normal(self):
        '''Tests read endpoints for normal YAML file'''
        endpoints = read_endpoints('normalfile.yml')
        self.assertIsNotNone(endpoints)
        self.assertEqual(endpoints, YML_DATA)
