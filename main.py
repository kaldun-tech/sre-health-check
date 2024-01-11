from scripts.endpoint_reader import EndpointReader
from scripts.http_requests import HTTPRequester
from scripts.availability import AvailabilityMetrics
from argparse import ArgumentParser
import sys
import time

def do_query_report(metrics : AvailabilityMetrics, endpoints : dict):
    '''Query and report on endpoints'''
    responses = HTTPRequester.query_endpoints(endpoints)
    metrics.update_for_list(responses)
    metrics.report_metrics()

def main():
    '''Main entry point'''
    parser = ArgumentParser(description='Query and report on endpoints')
    parser.add_argument('-f', '--filename', type=str, help='YAML file containing endpoint definitions', required=False)
    args = parser.parse_args()

    endpoints = EndpointReader.read_endpoints(args.filename)
    if endpoints is None:
        print('ERROR: Failed to read endpoints')
        sys.exit(1)

    sleeptime = 15
    metrics = AvailabilityMetrics()
    print(f'Found {len(endpoints)} endpoints')
    print(f'Program will query endpoints and report results every {sleeptime} seconds, press CTRL + C to quit...')
    while True:
        do_query_report(metrics, endpoints)
        time.sleep(sleeptime)

if __name__ == '__main__':
    main()
