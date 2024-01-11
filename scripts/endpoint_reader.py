import yaml
import os

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
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise('File not found: ' + file_path)
        except yaml.YAMLError as e:
            raise('Error parsing YAML: ' + str(e))
