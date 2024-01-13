import os
import yaml

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'data', 'endpoints.yml')

class EndpointReader:
    '''Reads REST endpoints from YAML file'''

    @staticmethod
    def read_endpoints(file_path : str = DEFAULT_FILE_PATH) -> dict | None:
        '''Read endpoints from YAML file
        Args:
            file_path (str): Path to the YAML file
        Returns:
            dict: The parsed YAML file as dictionary, None on failure
        Raises:
            FileNotFoundError: File was not found
            yaml.YAMLError: Failed to parse errors
        '''
        if file_path is None:
            file_path = DEFAULT_FILE_PATH
        with open(file_path, 'r', encoding='utf8') as file:
            return yaml.safe_load(file)
