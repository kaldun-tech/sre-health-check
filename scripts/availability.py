from http_requests import HTTPRequester
from requests import Response

class AvailabilityMetrics():
    '''Computes and reports availability metrics for endpoint domains'''

    def __init__(self):
        '''Constructor for AvailabilityCheck'''
        # Maps domain to Tuple: (up_count, total_count)
        self.availability_dict = {}

    def get_availability(self, domain: str):
        '''Get availability for domain as Tuple (up_count, total_count)'''
        return self.availability_dict[domain] if domain in self.availability_dict.keys() else (0, 0)

    def update_availability(self, domain : str, status_code, latency):
        '''Update availability for domain and Response status code'''
        availability = self.get_availability(domain)
        if 200 <= status_code < 300 and latency < 500:
            # Increment up count
            availability[0] += 1
        # Increment total count
        availability[1] += 1
        # Update cache
        self.availability_dict[domain] = availability

    def get_percent_available(self, domain : str):
        '''Computes the availability percentage for a domain, 0 for not found'''
        (up_count, total_count) = self.get_availability(domain)
        return 100 * up_count / total_count if 0 < total_count else 0

    def update_metrics(self, response : Response):
        '''Updates metrics for individual Response'''
        domain = HTTPRequester.get_endpoint_domain(response.url)
        status_code = response.status_code
        latency = response.elapsed
        self.update_availability(domain, status_code, latency)

    def handle_response_list(self, responses : list):
        '''Updates availability metrics for list of Responses and reports results'''
        for next_resp in responses:
            self.update_metrics(next_resp)
        for domain in self.availability_dict.keys():
            percent_available = self.get_percent_available(domain)
            print(f'{domain} has {percent_available}% availability percentage')
            