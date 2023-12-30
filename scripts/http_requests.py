import requests

class HTTPRequester:
    '''Performs HTTP requests'''

    @staticmethod
    def query_endpoints(endpoints : dict):
        '''Queries all endpoints in collection
        Arguments:
            endpoints (dict): Dictionary of requests to query
        Returns:
            list: Responses to requests'''
        responses = []
        for endpoint_name, endpoint_data in endpoints.items():
            url = endpoint_data['url']
            method = endpoint_data.get('method', 'GET')  # Default to GET if not specified
            headers = endpoint_data.get('headers', {})
            params = endpoint_data.get('params', {})
            data = endpoint_data.get('data', {})
            next_resp = HTTPRequester.query_endpoint(url, method, headers, params, data)
            responses.append(next_resp)

        return responses

    @staticmethod
    def query_endpoint(url, method='GET', headers=None, params=None, data=None):
        '''Query single endpoint
        Arguments:
            url: URL string to query
            method: HTTP method, default is GET
            headers: HTTP headers, default None
            params: HTTP parameters, default None
            data: HTTP POST data, default None
        Returns: Response to request'''
        return requests.request(method, url, headers=headers, params=params, data=data)

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
