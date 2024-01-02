from datetime import timedelta
from scripts.http_requests import EndpointResponse

class MockResponse(EndpointResponse):
    '''Mock response object for testing'''
    ELAPSED_ZERO = timedelta(0)
    ELAPSED_MAX = timedelta(milliseconds=499)
    ELAPSED_HIGH = timedelta(milliseconds=500)
