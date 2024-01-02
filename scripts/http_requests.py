import requests
from datetime import timedelta

class EndpointResponse:
    '''Endpoint response'''
    def __init__(self, name : str, url : str, status_code : int, elapsed : timedelta):
        self.name = name
        self.url = url
        self.status_code = status_code
        self.elapsed = elapsed

class HTTPRequester:
    '''Performs HTTP requests'''

    @staticmethod
    def query_endpoints(endpoints : dict) -> list:
        '''Queries all endpoints in collection
        Arguments:
            endpoints (dict): Dictionary of requests to query
        Returns:
            list: Responses to requests'''
        responses = []
        for next_endpoint in endpoints:
            name = next_endpoint['name']
            url = next_endpoint['url']
            method = next_endpoint.get('method', 'GET')  # Default to GET if not specified
            headers = next_endpoint.get('headers', None)
            json = next_endpoint.get('body', None)
            response = HTTPRequester.query_endpoint(url, method, headers, json)
            responses.append(EndpointResponse(name, url, response.status_code, response.elapsed))

        return responses

    @staticmethod
    def query_endpoint(url, method='GET', headers=None, json=None):
        '''Query single endpoint
        Arguments:
            url: URL string to query
            method: HTTP method, default is GET
            headers: HTTP headers, default None
            json: Request body, default None
        
        Returns: Response to request'''
        return requests.request(method, url, headers=headers, json=json)

    @staticmethod
    def get_endpoint_domain(url : str):
        '''Get domain for an endpoint URL
        Arguments:
            url: URL string
        Returns: domain string, empty for None input'''
        if url is None:
            return ''

        # Advanced past http:// or https://
        prefixes = ['http://', 'https://']
        for prefix in prefixes:
            if url.startswith(prefix):
                url = url[len(prefix):]
                break

        # Truncate at separator /
        endIndex = url.find('/')
        if -1 < endIndex:
            return url[:endIndex]

        return url
