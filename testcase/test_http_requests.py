from unittest import TestCase
from unittest.mock import patch
from scripts.http_requests import EndpointResponse
from scripts.http_requests import HTTPRequester
from testcase.mock_response import MockResponse

MOCK_ENDPOINTS = [
    {'name': 'up', 'url': 'up.com', 'method' : 'GET'},
    {'name': 'slow', 'url': 'slow.com', 'method' : 'POST'},
    {'name': 'down', 'url': 'down.com', 'method' : 'GET'},
]
MOCK_RESPONSES = {
    'up.com' : EndpointResponse('up', 'up.com', 200, MockResponse.ELAPSED_MAX),
    'slow.com' : EndpointResponse('slow', 'slow.com', 200, MockResponse.ELAPSED_HIGH),
    'down.com' : EndpointResponse('down', 'down.com', 500, MockResponse.ELAPSED_MAX),
}

class MockRequest():
    '''Mock request object for testing'''
    def __init__(self, url, method):
        self.url = url
        self.method = method

    @staticmethod
    # pylint: disable=unused-argument
    def request(method, url, **kwargs):
        '''Mock request method'''
        return MOCK_RESPONSES[url] if url in MOCK_RESPONSES else MockResponse(url, url, 404, MockResponse.ELAPSED_MAX)


class TestHTTPRequester(TestCase):
    '''Tests for HTTPRequester'''

    def test_query_endpoints_none(self):
        '''Test query of None endpoints dictionary'''
        responses = HTTPRequester.query_endpoints(None)
        self.assertIsNotNone(responses)
        self.assertEqual(responses, [])

    def test_query_endpoints_empty(self):
        '''Test query of empty endpoints dictionary'''
        responses = HTTPRequester.query_endpoints({})
        self.assertIsNotNone(responses)
        self.assertEqual(responses, [])

    def test_query_endpoints_invalid(self):
        '''Test query of invalid endpoints dictionary'''
        responses = HTTPRequester.query_endpoints({None})
        self.assertIsNotNone(responses)
        self.assertEqual(responses, [])

    @patch('requests.request', MockRequest.request)
    def test_query_endpoints_normal(self):
        '''Testing non-empty query endpoints would require a mock'''
        responses = HTTPRequester.query_endpoints(MOCK_ENDPOINTS)
        self.assertIsNotNone(responses)
        self.assertEqual(len(responses), len(MOCK_ENDPOINTS))
        for response in responses:
            self.assertIsNotNone(response)
            mock_res = MOCK_RESPONSES[response.url]
            self.assertIsNotNone(mock_res)
            self.assertEqual(mock_res.name, response.name)
            self.assertEqual(mock_res.status_code, response.status_code)
            self.assertEqual(mock_res.elapsed, response.elapsed)

    def test_query_endpoint_none(self):
        '''Tests for query endpoint with None input'''
        response = HTTPRequester.query_endpoint(None)
        self.assertIsNone(response)

    def test_query_endpoint_malformed(self):
        '''Tests for query malformed endpoint'''
        response = HTTPRequester.query_endpoint('fake.news')
        self.assertIsNone(response)

    def test_query_endpoint_nonexistent(self):
        '''Tests for query bad request'''
        response = HTTPRequester.query_endpoint('https://google.com/fakenews')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    def test_query_endpoint_normal(self):
        '''Tests for query normal endpoint'''
        response = HTTPRequester.query_endpoint('https://jsonplaceholder.typicode.com/todos/1')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    def test_get_endpoint_domain_degen(self):
        '''Tests for get endpoint domain None/empty'''
        exp_domain = ''
        act_domain = HTTPRequester.get_endpoint_domain(None)
        self.assertEqual(exp_domain, act_domain)
        act_domain = HTTPRequester.get_endpoint_domain('')
        self.assertEqual(exp_domain, act_domain)

    def test_get_endpoint_domain_normal(self):
        '''Tests for get endpoint domain non-empty'''
        exp_domain = 'jsonplaceholder.typicode.com'
        act_domain = HTTPRequester.get_endpoint_domain('jsonplaceholder.typicode.com')
        self.assertEqual(exp_domain, act_domain)
        act_domain = HTTPRequester.get_endpoint_domain('jsonplaceholder.typicode.com/posts')
        self.assertEqual(exp_domain, act_domain)
        act_domain = HTTPRequester.get_endpoint_domain('www.jsonplaceholder.typicode.com')
        self.assertEqual(exp_domain, act_domain)
        act_domain = HTTPRequester.get_endpoint_domain('http://jsonplaceholder.typicode.com')
        self.assertEqual(exp_domain, act_domain)
        act_domain = HTTPRequester.get_endpoint_domain('https://jsonplaceholder.typicode.com')
        self.assertEqual(exp_domain, act_domain)
        act_domain = HTTPRequester.get_endpoint_domain('https://www.jsonplaceholder.typicode.com/posts')
        self.assertEqual(exp_domain, act_domain)
