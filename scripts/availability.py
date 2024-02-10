'''Availability metrics for endpoint domains'''
from datetime import timedelta
from scripts.http_requests import HTTPRequester

class AvailabilityMetrics():
    '''Computes and reports availability metrics for endpoint domains'''

    def __init__(self):
        '''Constructor for AvailabilityCheck'''
        # Maps domain to Tuple: (up_count, down_count)
        self.availability_dict = {}

    def get_availability(self, domain: str) -> dict:
        '''Get availability for domain as Tuple (up_count, down_count)'''
        return self.availability_dict[domain] if domain in self.availability_dict else (0, 0)

    @staticmethod
    def is_endpoint_up(status_code : int, elapsed : timedelta) -> bool:
        '''Test if endpoint is up
        Arguments:
            status_code: Query status code, considered up from 200 to 299
            elapsed_ms: Query elapsed timedelta, considered up for less than 500 ms
        Returns:
            True if endpoint is up, False otherwise
        '''
        return 200 <= status_code < 300 and elapsed < timedelta(milliseconds=500)

    def get_percent_available(self, domain : str) -> int:
        '''Computes the availability percentage for a domain, 0 for not found
        Arguments:
            domain: Domain to check
        Returns: Availability percentage as int
        '''
        (up_count, down_count) = self.get_availability(domain)
        total_count = up_count + down_count
        return round(100 * up_count / total_count) if 0 < total_count else 0

    def update_for_domain(self, domain : str, status_code : int, elapsed : timedelta):
        '''Update availability for domain, status code, and elapsed millis
        Arguments:
            domain: Domain to update availability for
            status_code: Query status code, considered up from 200 to 299
            elapsed: Query elapsed timedelta, considered up for less than 500 ms
        '''
        (up, down) = self.get_availability(domain)
        if AvailabilityMetrics.is_endpoint_up(status_code, elapsed):
            # Increment up count
            up += 1
        else:
            # Increment down count
            down += 1
        # Update cache
        self.availability_dict[domain] = (up, down)

    def update_for_response(self, response):
        '''Updates metrics for individual request response
        Arguments:
            response: Single response to update metrics for'''
        domain = HTTPRequester.get_endpoint_domain(response.url)
        self.update_for_domain(domain, response.status_code, response.elapsed)

    def update_for_list(self, responses : list):
        '''Updates availability metrics for list of Responses
        Arguments:
            responses: List of responses to update metrics for'''
        for next_resp in responses:
            self.update_for_response(next_resp)

    def report_metrics(self):
        '''Prints out availability metrics'''
        for domain in self.availability_dict:
            percent_available = self.get_percent_available(domain)
            print(f'{domain} has {percent_available}% availability percentage')
