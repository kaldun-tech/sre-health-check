from scripts.endpoint_reader import EndpointReader
from scripts.http_requests import HTTPRequester
from scripts.availability import AvailabilityMetrics
import sys
import time

def main():
    '''Main entry point'''
    endpoints = EndpointReader.read_endpoints()
    if endpoints is None:
        print('ERROR: Failed to read endpoints')
        sys.exit(1)

    sleeptime = 15
    metrics = AvailabilityMetrics()
    print(f'Found {len(endpoints)} endpoints')
    print(f'Program will query endpoints and report results every {sleeptime} seconds, press CTRL + C to quit...')
    while True:
        responses = HTTPRequester.query_endpoints(endpoints)
        metrics.update_for_list(responses)
        metrics.report_metrics()
        time.sleep(sleeptime)

if __name__ == '__main__':
    main()
