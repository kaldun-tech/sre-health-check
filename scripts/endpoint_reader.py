import yaml
import os

class EndpointReader:
    '''Reads REST endpoints from YAML file'''

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DEFAULT_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'data', 'fetch.yml')

    def read_endpoints(file_path : str = DEFAULT_FILE_PATH):
        with open(file_path, 'r') as file:
            endpoints = yaml.safe_load(file)
        return endpoints
