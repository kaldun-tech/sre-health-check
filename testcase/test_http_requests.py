from scripts.http_requests import HTTPRequester
from unittest import TestCase

class TestHTTPRequester(TestCase):
    '''Tests for HTTPRequester'''

    def test_query_endpoints(self):
        pass

    def test_query_endpoint(self):
        pass

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
