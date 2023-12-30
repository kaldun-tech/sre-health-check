import yaml
import os

class EndpointReader:
    '''Reads REST endpoints from YAML file'''

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DEFAULT_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'data', 'fetch.yml')

    @staticmethod
    def read_endpoints(file_path : str = DEFAULT_FILE_PATH):
        '''Read endpoints from YAML file
        Args:
            file_path (str): Path to the YAML file
        Returns:
            dict: The parsed YAML file as dictionary
        Raises:
            FileNotFoundError: If the file does not exist
            yaml.YAMLError: If there is an error parsing the YAML'''
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError('File not found: ' + file_path)
        except yaml.YAMLError as e:
            raise yaml.YAMLError('Error parsing YAML: ' + str(e))
