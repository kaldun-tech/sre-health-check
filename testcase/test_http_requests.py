from unittest import TestCase
from scripts.http_requests import EndpointResponse
from scripts.http_requests import HTTPRequester
from testcase.mock_response import MockResponse
from unittest.mock import patch

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

    def request(method, url, **kwargs):
        '''Mock request method'''
        if url in MOCK_RESPONSES.keys():
            return MOCK_RESPONSES[url]
        else:
            return MockResponse(url, url, 404, MockResponse.ELAPSED_MAX)


class TestHTTPRequester(TestCase):
    '''Tests for HTTPRequester'''

    def test_query_endpoints_empty(self):
        '''Test query of empty endpoints dictionary'''
        responses = HTTPRequester.query_endpoints({})
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
            self.assertEquals(mock_res.name, response.name)
            self.assertEquals(mock_res.status_code, response.status_code)
            self.assertEquals(mock_res.elapsed, response.elapsed)

    # Skipping test_query_endpoint as this just passes through to requests

    def test_get_endpoint_domain_degen(self):
        '''Tests for get endpoint domain None/empty'''
        exp_domain = ''
        act_domain = HTTPRequester.get_endpoint_domain(None)
        self.assertEqual(exp_domain, act_domain)
        act_domain = HTTPRequester.get_endpoint_domain('')
        self.assertEqual(exp_domain, act_domain)

    def test_get_endpoint_domain_normal(self):
        '''Tests for get endpoint domain non-empty'''
        exp_domain = 'www.fetch.com'
        act_domain = HTTPRequester.get_endpoint_domain('www.fetch.com')
        self.assertEqual(exp_domain, act_domain)
        act_domain = HTTPRequester.get_endpoint_domain('www.fetch.com/careers')
        self.assertEqual(exp_domain, act_domain)
        act_domain = HTTPRequester.get_endpoint_domain('http://www.fetch.com')
        self.assertEqual(exp_domain, act_domain)
        act_domain = HTTPRequester.get_endpoint_domain('http://www.fetch.com/some/url')
        self.assertEqual(exp_domain, act_domain)
        act_domain = HTTPRequester.get_endpoint_domain('https://www.fetch.com/')
        self.assertEqual(exp_domain, act_domain)
        act_domain = HTTPRequester.get_endpoint_domain('https://www.fetch.com/careers')
        self.assertEqual(exp_domain, act_domain)
        act_domain = HTTPRequester.get_endpoint_domain('https://www.fetch.com/some/post/url')
        self.assertEqual(exp_domain, act_domain)
