from unittest import TestCase
from scripts.availability import AvailabilityMetrics
from testcase.mock_response import MockResponse

class TestAvailabilityMetrics(TestCase):
    '''Tests for AvailabilityMetrics'''

    def setUp(self):
        '''Sets up the AvailabilityMetrics object'''
        self.metrics = AvailabilityMetrics()
        self.metrics.availability_dict['up.com'] = (1, 0)
        self.metrics.availability_dict['down.com'] = (0, 1)
        self.metrics.availability_dict['sometimes.com'] = (3, 1)

    def test_is_endpoint_up_statuscode(self):
        '''Tests is_endpoint_up for various status codes'''
        self.assertFalse(AvailabilityMetrics.is_endpoint_up(199, MockResponse.ELAPSED_ZERO))
        self.assertTrue(AvailabilityMetrics.is_endpoint_up(200, MockResponse.ELAPSED_ZERO))
        self.assertTrue(AvailabilityMetrics.is_endpoint_up(299, MockResponse.ELAPSED_ZERO))
        self.assertFalse(AvailabilityMetrics.is_endpoint_up(300, MockResponse.ELAPSED_ZERO))
        self.assertFalse(AvailabilityMetrics.is_endpoint_up(404, MockResponse.ELAPSED_ZERO))

    def test_is_endpoint_up_elapsed(self):
        '''Tests is_endpoint_up by varying elapsed for good status code'''
        self.assertTrue(AvailabilityMetrics.is_endpoint_up(200, MockResponse.ELAPSED_ZERO))
        self.assertTrue(AvailabilityMetrics.is_endpoint_up(200, MockResponse.ELAPSED_MAX))
        self.assertFalse(AvailabilityMetrics.is_endpoint_up(200, MockResponse.ELAPSED_HIGH))

    def test_update_availability_for_domain(self):
        '''Tests updating and getting availability for single response'''
        self.metrics.update_for_response(MockResponse('fetch', 'fetch.com', 200, MockResponse.ELAPSED_ZERO))
        (up, down) = self.metrics.get_availability('fetch.com')
        self.assertEqual(up, 1)
        self.assertEqual(down, 0)

    def test_update_availability_for_list(self):
        '''Tests updating and getting availability for list of responses'''
        responses = [
            MockResponse('fast', 'fetch.com', 200, MockResponse.ELAPSED_ZERO),
            MockResponse('slow', 'fetch.com', 299, MockResponse.ELAPSED_MAX),
            MockResponse('down', 'fetch.com', 300, MockResponse.ELAPSED_ZERO),
        ]
        self.metrics.update_for_list(responses)
        (up, down) = self.metrics.get_availability('fetch.com')
        self.assertEqual(up, 2)
        self.assertEqual(down, 1)
        self.assertEqual(self.metrics.get_percent_available('fetch.com'), round(200.0 / 3))

    def test_get_percent_available(self):
        '''Tests get percent available from initial setup'''
        self.assertEqual(self.metrics.get_percent_available('up.com'), 100)
        self.assertEqual(self.metrics.get_percent_available('down.com'), 0)
        self.assertEqual(self.metrics.get_percent_available('notpresent.com'), 0)
        self.assertEqual(self.metrics.get_percent_available('sometimes.com'), 75)
        self.metrics.report_metrics()
