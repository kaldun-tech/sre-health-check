from scripts.endpoint_reader import EndpointReader
from scripts.http_requests import HTTPRequester
from scripts.availability import AvailabilityMetrics
import sys
import time

def do_query_report(metrics : AvailabilityMetrics, endpoints : dict):
    '''Query and report on endpoints'''
    responses = HTTPRequester.query_endpoints(endpoints)
    metrics.update_for_list(responses)
    metrics.report_metrics()

def main():
    '''Main entry point'''
    endpoints = EndpointReader.read_endpoints()
    if endpoints is None:
        print('ERROR: Failed to read endpoints')
        sys.exit(1)

    sleeptime = 15
    paused = False
    metrics = AvailabilityMetrics()
    print(f'Found {len(endpoints)} endpoints')
    print(f'Program will query endpoints and report results every {sleeptime} seconds, press CTRL + C to quit...')
    while True:
        do_query_report(metrics, endpoints)
        time.sleep(sleeptime)

if __name__ == '__main__':
    main()
