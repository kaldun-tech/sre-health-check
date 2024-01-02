from scripts.availability import AvailabilityMetrics
from unittest import TestCase
from datetime import timedelta

ELAPSED_ZERO = timedelta(0)
ELAPSED_MAX = timedelta(milliseconds=499)
ELAPSED_HIGH = timedelta(milliseconds=500)

class MockResponse():
    '''Mock response object for testing'''
    def __init__(self, url, status_code, elapsed):
        self.url = url
        self.status_code = status_code
        self.elapsed = elapsed

    def url(self):
        return self.url

    def status_code(self):
        return self.status_code

    def elapsed(self):
        return self.elapsed


class TestAvailabilityMetrics(TestCase):
    '''Tests for AvailabilityMetrics'''

    def setUp(self):
        '''Sets up the AvailabilityMetrics object'''
        self.metrics = AvailabilityMetrics()
        self.metrics.availability_dict['alwaysup.com'] = (1, 0)
        self.metrics.availability_dict['alwaysdown.com'] = (0, 1)
        self.metrics.availability_dict['sometimesup.com'] = (3, 1)

    def test_is_endpoint_up_statuscode(self):
        '''Tests is_endpoint_up for various status codes'''
        self.assertFalse(AvailabilityMetrics.is_endpoint_up(199, ELAPSED_ZERO))
        self.assertTrue(AvailabilityMetrics.is_endpoint_up(200, ELAPSED_ZERO))
        self.assertTrue(AvailabilityMetrics.is_endpoint_up(299, ELAPSED_ZERO))
        self.assertFalse(AvailabilityMetrics.is_endpoint_up(300, ELAPSED_ZERO))
        self.assertFalse(AvailabilityMetrics.is_endpoint_up(404, ELAPSED_ZERO))

    def test_is_endpoint_up_elapsed(self):
        '''Tests is_endpoint_up by varying elapsed for good status code'''
        self.assertTrue(AvailabilityMetrics.is_endpoint_up(200, ELAPSED_ZERO))
        self.assertTrue(AvailabilityMetrics.is_endpoint_up(200, ELAPSED_MAX))
        self.assertFalse(AvailabilityMetrics.is_endpoint_up(200, ELAPSED_HIGH))

    def test_update_availability_for_domain(self):
        '''Tests updating and getting availability for single response'''
        self.metrics.update_for_response(MockResponse('fetch.com', 200, ELAPSED_ZERO))
        (up, down) = self.metrics.get_availability('fetch.com')
        self.assertEquals(up, 1)
        self.assertEquals(down, 0)

    def test_update_availability_for_list(self):
        '''Tests updating and getting availability for list of responses'''
        responses = [
            MockResponse('fetch.com', 200, ELAPSED_ZERO),
            MockResponse('fetch.com', 299, ELAPSED_MAX),
            MockResponse('fetch.com', 300, ELAPSED_ZERO),
        ]
        self.metrics.update_for_list(responses)
        (up, down) = self.metrics.get_availability('fetch.com')
        self.assertEquals(up, 2)
        self.assertEquals(down, 1)
        self.assertEquals(self.metrics.get_percent_available('fetch.com'), 200.0 / 3)
    
    def test_get_percent_available(self):
        '''Tests get percent available from initial setup'''
        self.assertEqual(self.metrics.get_percent_available('alwaysup.com'), 100.0)
        self.assertEqual(self.metrics.get_percent_available('alwaysdown.com'), 0.0)
        self.assertEqual(self.metrics.get_percent_available('notpresent.com'), 0.0)
        self.assertEqual(self.metrics.get_percent_available('sometimesup.com'), 75.0)
        self.metrics.report_metrics()
