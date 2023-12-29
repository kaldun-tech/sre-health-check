import requests

class HTTPRequester:
    '''Performs HTTP requests'''

    def query_endpoints(self, endpoints):
        '''Queries all endpoints in collection'''
        responses = []
        for endpoint_name, endpoint_data in endpoints.items():
            url = endpoint_data['url']
            method = endpoint_data.get('method', 'GET')  # Default to GET if not specified
            headers = endpoint_data.get('headers', {})
            params = endpoint_data.get('params', {})
            data = endpoint_data.get('data', {})
            next_resp = self.query_endpoint(url, method, headers, params, data)
            responses.append(next_resp)

        return responses


    def query_endpoint(self, url, method='GET', headers=None, params=None, data=None):
        '''Query single endpoint'''
        return requests.request(method, url, headers=headers, params=params, data=data)
